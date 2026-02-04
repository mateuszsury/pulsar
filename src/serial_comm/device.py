"""Device abstraction for serial communication."""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable

import serial_asyncio

logger = logging.getLogger(__name__)


class DeviceState(Enum):
    """Device connection state."""

    DISCONNECTED = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    BUSY = auto()
    ERROR = auto()


@dataclass
class DeviceInfo:
    """Information about a connected device."""

    port: str
    baudrate: int = 115200
    state: DeviceState = DeviceState.DISCONNECTED
    firmware: str = ""
    machine: str = ""
    platform: str = ""
    connected_at: datetime | None = None
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "port": self.port,
            "baudrate": self.baudrate,
            "state": self.state.name.lower(),
            "firmware": self.firmware,
            "machine": self.machine,
            "platform": self.platform,
            "connected_at": self.connected_at.isoformat() if self.connected_at else None,
            "error": self.error,
        }


class Device:
    """Represents a connected ESP32/MicroPython device."""

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        on_output: Callable[[str], None] | None = None,
    ) -> None:
        self.info = DeviceInfo(port=port, baudrate=baudrate)
        self._on_output = on_output

        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._read_task: asyncio.Task[None] | None = None
        self._lock = asyncio.Lock()
        self._output_buffer: list[str] = []

        # Reading control - stop read loop during direct operations
        self._read_lock = asyncio.Lock()  # Lock for exclusive reading
        self._read_loop_stopped = False  # Flag to stop read loop

    @property
    def port(self) -> str:
        """Get device port."""
        return self.info.port

    @property
    def state(self) -> DeviceState:
        """Get device state."""
        return self.info.state

    @property
    def is_connected(self) -> bool:
        """Check if device is connected."""
        return self.info.state == DeviceState.CONNECTED

    async def connect(self) -> bool:
        """Connect to the device."""
        if self.info.state != DeviceState.DISCONNECTED:
            return False

        self.info.state = DeviceState.CONNECTING
        logger.info("Connecting to %s at %d baud", self.port, self.info.baudrate)

        try:
            self._reader, self._writer = await serial_asyncio.open_serial_connection(
                url=self.port,
                baudrate=self.info.baudrate,
            )

            # Start reading task
            self._read_task = asyncio.create_task(self._read_loop())

            # Get device info
            await self._get_device_info()

            self.info.state = DeviceState.CONNECTED
            self.info.connected_at = datetime.now()
            logger.info("Connected to %s", self.port)
            return True

        except Exception as e:
            self.info.state = DeviceState.ERROR
            self.info.error = str(e)
            logger.error("Failed to connect to %s: %s", self.port, e)
            return False

    async def disconnect(self) -> None:
        """Disconnect from the device."""
        if self._read_task:
            self._read_task.cancel()
            try:
                await self._read_task
            except asyncio.CancelledError:
                pass

        if self._writer:
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception:
                pass

        self._reader = None
        self._writer = None
        self.info.state = DeviceState.DISCONNECTED
        self.info.connected_at = None
        logger.info("Disconnected from %s", self.port)

    async def write(self, data: bytes) -> None:
        """Write data to the device."""
        if not self._writer:
            raise RuntimeError("Device not connected")

        async with self._lock:
            self._writer.write(data)
            await self._writer.drain()

    async def write_line(self, text: str) -> None:
        """Write a line to the device."""
        await self.write((text + "\r\n").encode())

    async def pause_read_loop(self) -> None:
        """Stop the background read loop for exclusive reading."""
        await self._read_lock.acquire()
        # Cancel and wait for read task to stop
        if self._read_task and not self._read_task.done():
            self._read_loop_stopped = True
            self._read_task.cancel()
            try:
                await self._read_task
            except asyncio.CancelledError:
                pass
        logger.debug("Read loop paused for %s", self.port)

    def resume_read_loop(self) -> None:
        """Restart the background read loop."""
        self._read_loop_stopped = False
        # Restart read task
        if self._reader and not self._reader.at_eof():
            self._read_task = asyncio.create_task(self._read_loop())
        if self._read_lock.locked():
            self._read_lock.release()
        logger.debug("Read loop resumed for %s", self.port)

    async def read(self, size: int = 1024, timeout: float = 1.0) -> bytes:
        """Read data from the device (assumes read loop is paused or will pause it)."""
        if not self._reader:
            raise RuntimeError("Device not connected")

        # If lock is held, we're in a batch operation - just read
        owns_lock = False
        if not self._read_lock.locked():
            await self.pause_read_loop()
            owns_lock = True

        try:
            return await asyncio.wait_for(
                self._reader.read(size),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            return b""
        finally:
            if owns_lock:
                self.resume_read_loop()

    async def read_until(
        self,
        expected: bytes,
        timeout: float = 5.0,
    ) -> bytes:
        """Read until expected bytes are found."""
        if not self._reader:
            raise RuntimeError("Device not connected")

        # If lock is held, we're in a batch operation - just read
        owns_lock = False
        if not self._read_lock.locked():
            await self.pause_read_loop()
            owns_lock = True

        try:
            return await asyncio.wait_for(
                self._reader.readuntil(expected),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            return b""
        except asyncio.IncompleteReadError as e:
            return e.partial
        finally:
            if owns_lock:
                self.resume_read_loop()

    async def interrupt(self) -> None:
        """Send Ctrl+C to interrupt current operation."""
        await self.write(b"\x03")

    async def reset(self, soft: bool = True) -> None:
        """Reset the device."""
        if soft:
            # Soft reset via Ctrl+D
            await self.write(b"\x04")
        else:
            # Hard reset via machine.reset()
            await self.write_line("import machine; machine.reset()")

    async def _read_loop(self) -> None:
        """Continuously read from the device."""
        logger.debug("Read loop started for %s", self.port)
        while self._reader and not self._reader.at_eof() and not self._read_loop_stopped:
            try:
                # Use a short timeout to allow clean cancellation
                try:
                    data = await asyncio.wait_for(
                        self._reader.read(1024),
                        timeout=0.1,
                    )
                except asyncio.TimeoutError:
                    continue

                if data:
                    text = data.decode("utf-8", errors="replace")
                    logger.debug("Read loop received %d bytes: %s", len(data), text[:50] if len(text) > 50 else text)
                    self._output_buffer.append(text)

                    # Limit buffer size
                    while len(self._output_buffer) > 1000:
                        self._output_buffer.pop(0)

                    if self._on_output:
                        self._on_output(text)

            except asyncio.CancelledError:
                logger.debug("Read loop cancelled for %s", self.port)
                break
            except Exception as e:
                if not self._read_loop_stopped:
                    logger.exception("Read error on %s: %s", self.port, e)
                    self.info.state = DeviceState.ERROR
                    self.info.error = str(e)
                break

        logger.debug("Read loop ended for %s", self.port)

    async def _get_device_info(self) -> None:
        """Get device information."""
        await self.pause_read_loop()
        try:
            # Send Ctrl+C to ensure clean state
            await self.write(b"\x03")
            await asyncio.sleep(0.1)

            # Clear any pending output
            await self.read(timeout=0.2)

            # Get sys info
            await self.write_line("import sys; print(sys.version, sys.platform)")
            await asyncio.sleep(0.1)
            response = await self.read(timeout=0.5)
            text = response.decode("utf-8", errors="replace")

            if "micropython" in text.lower():
                self.info.platform = "micropython"
                # Parse version info
                lines = text.strip().split("\n")
                for line in lines:
                    if "MicroPython" in line:
                        self.info.firmware = line.strip()
                        break

            # Get machine info
            await self.write_line("import os; print(os.uname())")
            await asyncio.sleep(0.1)
            response = await self.read(timeout=0.5)
            text = response.decode("utf-8", errors="replace")
            if "machine=" in text:
                # Parse machine from uname output
                for part in text.split(","):
                    if "machine=" in part:
                        self.info.machine = part.split("=")[1].strip("'\")")

        except Exception as e:
            logger.warning("Failed to get device info: %s", e)
        finally:
            self.resume_read_loop()

    def get_output(self, clear: bool = False) -> str:
        """Get buffered output."""
        output = "".join(self._output_buffer)
        if clear:
            self._output_buffer.clear()
        return output
