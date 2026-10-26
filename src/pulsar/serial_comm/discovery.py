"""Port discovery and scanning."""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

import serial.tools.list_ports
from serial.tools.list_ports_common import ListPortInfo

logger = logging.getLogger(__name__)


@dataclass
class PortInfo:
    """Information about a serial port."""

    port: str
    description: str
    hwid: str
    vid: int | None
    pid: int | None
    manufacturer: str | None
    product: str | None
    serial_number: str | None

    @classmethod
    def from_list_port_info(cls, info: ListPortInfo) -> "PortInfo":
        """Create PortInfo from pyserial ListPortInfo."""
        return cls(
            port=info.device,
            description=info.description or "",
            hwid=info.hwid or "",
            vid=info.vid,
            pid=info.pid,
            manufacturer=info.manufacturer,
            product=info.product,
            serial_number=info.serial_number,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "port": self.port,
            "description": self.description,
            "hwid": self.hwid,
            "vid": self.vid,
            "pid": self.pid,
            "manufacturer": self.manufacturer,
            "product": self.product,
            "serial_number": self.serial_number,
        }

    def is_esp32(self) -> bool:
        """Check if this port is likely an ESP32 device."""
        # Common ESP32 USB-Serial chip VIDs
        esp_vids = {
            0x10C4,  # Silicon Labs CP210x
            0x1A86,  # QinHeng Electronics CH340
            0x0403,  # FTDI
            0x303A,  # Espressif
        }
        if self.vid and self.vid in esp_vids:
            return True

        # Check description
        esp_keywords = ["cp210", "ch340", "ftdi", "esp32", "usb-serial"]
        desc_lower = self.description.lower()
        return any(kw in desc_lower for kw in esp_keywords)


class PortDiscovery:
    """Discover and monitor serial ports."""

    def __init__(self) -> None:
        self._known_ports: set[str] = set()
        self._running = False
        self._task: asyncio.Task[None] | None = None
        self._callbacks: list[Any] = []

    def scan(self) -> list[PortInfo]:
        """Scan for available serial ports."""
        ports = []
        for port_info in serial.tools.list_ports.comports():
            ports.append(PortInfo.from_list_port_info(port_info))
        return ports

    def scan_esp32(self) -> list[PortInfo]:
        """Scan for ESP32 devices only."""
        return [p for p in self.scan() if p.is_esp32()]

    def on_change(self, callback: Any) -> None:
        """Register callback for port changes."""
        self._callbacks.append(callback)

    async def start_monitoring(self, interval: float = 2.0) -> None:
        """Start monitoring for port changes."""
        if self._running:
            return

        self._running = True
        self._known_ports = {p.port for p in self.scan()}
        self._task = asyncio.create_task(self._monitor_loop(interval))
        logger.info("Port monitoring started")

    async def stop_monitoring(self) -> None:
        """Stop monitoring for port changes."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Port monitoring stopped")

    async def _monitor_loop(self, interval: float) -> None:
        """Monitor for port changes."""
        while self._running:
            try:
                await asyncio.sleep(interval)
                current_ports = {p.port for p in self.scan()}

                added = current_ports - self._known_ports
                removed = self._known_ports - current_ports

                if added or removed:
                    self._known_ports = current_ports
                    for callback in self._callbacks:
                        try:
                            if asyncio.iscoroutinefunction(callback):
                                await callback(list(added), list(removed))
                            else:
                                callback(list(added), list(removed))
                        except Exception as e:
                            logger.exception("Port change callback error: %s", e)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception("Port monitoring error: %s", e)
