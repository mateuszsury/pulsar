"""Multi-device serial manager."""

import asyncio
import logging
from typing import Any, Callable

from core.config import Config
from core.events import EventBus, EventType
from serial_comm.device import Device, DeviceState
from serial_comm.discovery import PortDiscovery, PortInfo
from serial_comm.file_transfer import FileTransfer
from serial_comm.repl import RawREPL, REPLResult

logger = logging.getLogger(__name__)


class SerialManager:
    """Manages multiple serial device connections."""

    def __init__(self, events: EventBus, config: Config) -> None:
        self.events = events
        self.config = config

        self._devices: dict[str, Device] = {}
        self._repls: dict[str, RawREPL] = {}
        self._file_transfers: dict[str, FileTransfer] = {}
        self._discovery = PortDiscovery()

    async def start(self) -> None:
        """Start the serial manager."""
        # Register for port changes
        self._discovery.on_change(self._on_ports_changed)
        await self._discovery.start_monitoring()

        # Emit initial port list
        ports = self._discovery.scan()
        self.events.emit(
            EventType.PORTS_UPDATED,
            {"ports": [p.to_dict() for p in ports]},
        )

        logger.info("Serial manager started")

    async def stop(self) -> None:
        """Stop the serial manager."""
        await self._discovery.stop_monitoring()

        # Disconnect all devices
        for port in list(self._devices.keys()):
            await self.disconnect(port)

        logger.info("Serial manager stopped")

    def scan_ports(self) -> list[PortInfo]:
        """Scan for available serial ports."""
        return self._discovery.scan()

    def scan_esp32_ports(self) -> list[PortInfo]:
        """Scan for ESP32 devices only."""
        return self._discovery.scan_esp32()

    def get_device(self, port: str) -> Device | None:
        """Get device by port."""
        return self._devices.get(port)

    def get_devices(self) -> list[Device]:
        """Get all connected devices."""
        return list(self._devices.values())

    async def connect(
        self,
        port: str,
        baudrate: int | None = None,
    ) -> bool:
        """Connect to a device."""
        if port in self._devices:
            logger.warning("Device already connected: %s", port)
            return True

        if baudrate is None:
            baudrate = self.config.default_baudrate

        # Create device with output callback
        def on_output(text: str) -> None:
            self.events.emit(
                EventType.DEVICE_OUTPUT,
                {"port": port, "text": text},
                source=port,
            )

        device = Device(port, baudrate, on_output=on_output)
        success = await device.connect()

        if success:
            self._devices[port] = device
            self._repls[port] = RawREPL(device)

            # Create file transfer with progress callback
            def on_progress(path: str, progress: float) -> None:
                self.events.emit(
                    EventType.FILE_PROGRESS,
                    {"port": port, "file": path, "progress": progress},
                    source=port,
                )

            self._file_transfers[port] = FileTransfer(
                self._repls[port],
                on_progress=on_progress,
            )

            self.events.emit(
                EventType.DEVICE_CONNECTED,
                {"port": port, "info": device.info.to_dict()},
                source=port,
            )
        else:
            self.events.emit(
                EventType.DEVICE_ERROR,
                {"port": port, "error": device.info.error},
                source=port,
            )

        return success

    async def disconnect(self, port: str) -> None:
        """Disconnect from a device."""
        device = self._devices.pop(port, None)
        self._repls.pop(port, None)
        self._file_transfers.pop(port, None)

        if device:
            await device.disconnect()
            self.events.emit(
                EventType.DEVICE_DISCONNECTED,
                {"port": port},
                source=port,
            )

    async def execute(
        self,
        port: str,
        code: str,
        timeout: float = 30.0,
    ) -> REPLResult:
        """Execute code on a device."""
        repl = self._repls.get(port)
        if not repl:
            return REPLResult(
                output="",
                error=f"Device not connected: {port}",
                success=False,
            )

        return await repl.execute(code, timeout=timeout)

    async def interrupt(self, port: str) -> bool:
        """Send interrupt (Ctrl+C) to device."""
        device = self._devices.get(port)
        if device:
            try:
                await device.interrupt()
                self.events.emit(
                    EventType.DEVICE_INTERRUPTED,
                    {"port": port, "success": True},
                    source=port,
                )
                return True
            except Exception as e:
                logger.error("Interrupt failed for %s: %s", port, e)
                self.events.emit(
                    EventType.DEVICE_INTERRUPTED,
                    {"port": port, "success": False, "error": str(e)},
                    source=port,
                )
                return False
        return False

    async def reset(self, port: str, soft: bool = True) -> bool:
        """Reset device."""
        repl = self._repls.get(port)
        if repl:
            try:
                success = await repl.soft_reset()
                self.events.emit(
                    EventType.DEVICE_RESET,
                    {"port": port, "success": success, "soft": soft},
                    source=port,
                )
                return success
            except Exception as e:
                logger.error("Reset failed for %s: %s", port, e)
                self.events.emit(
                    EventType.DEVICE_RESET,
                    {"port": port, "success": False, "soft": soft, "error": str(e)},
                    source=port,
                )
                return False
        return False

    async def list_files(self, port: str, path: str = "/") -> list[dict]:
        """List files on device."""
        ft = self._file_transfers.get(port)
        if not ft:
            return []

        files = await ft.list_files(path)
        return [f.to_dict() for f in files]

    async def read_file(self, port: str, path: str) -> bytes:
        """Read file from device."""
        ft = self._file_transfers.get(port)
        if not ft:
            raise RuntimeError(f"Device not connected: {port}")

        return await ft.read_file(path)

    async def write_file(
        self,
        port: str,
        path: str,
        content: bytes,
    ) -> bool:
        """Write file to device."""
        ft = self._file_transfers.get(port)
        if not ft:
            raise RuntimeError(f"Device not connected: {port}")

        success = await ft.write_file(path, content)

        if success:
            self.events.emit(
                EventType.FILE_UPLOADED,
                {"port": port, "path": path, "size": len(content)},
                source=port,
            )

        return success

    async def delete_file(self, port: str, path: str) -> bool:
        """Delete file from device."""
        ft = self._file_transfers.get(port)
        if not ft:
            return False

        success = await ft.delete_file(path)

        if success:
            self.events.emit(
                EventType.FILE_DELETED,
                {"port": port, "path": path},
                source=port,
            )

        return success

    async def mkdir(self, port: str, path: str) -> bool:
        """Create directory on device."""
        ft = self._file_transfers.get(port)
        if not ft:
            return False

        return await ft.mkdir(path)

    async def _on_ports_changed(
        self,
        added: list[str],
        removed: list[str],
    ) -> None:
        """Handle port changes."""
        # Disconnect removed devices
        for port in removed:
            if port in self._devices:
                await self.disconnect(port)
                logger.info("Device removed: %s", port)

        # Notify about new ports
        for port in added:
            logger.info("New port discovered: %s", port)
            self.events.emit(
                EventType.DEVICE_DISCOVERED,
                {"port": port},
            )

        # Emit updated port list
        ports = self._discovery.scan()
        self.events.emit(
            EventType.PORTS_UPDATED,
            {"ports": [p.to_dict() for p in ports]},
        )
