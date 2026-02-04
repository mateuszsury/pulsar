"""Type stubs for MicroPython onewire module (1-Wire protocol)."""

from typing import List, Optional
from machine import Pin


class OneWire:
    """1-Wire bus protocol interface.

    Used for devices like DS18B20 temperature sensors.

    Example:
        from machine import Pin
        import onewire

        ow = onewire.OneWire(Pin(4))
        devices = ow.scan()
        print(f"Found {len(devices)} devices")
    """

    SEARCH_ROM: int
    MATCH_ROM: int
    SKIP_ROM: int

    def __init__(self, pin: Pin) -> None:
        """Create 1-Wire interface.

        Args:
            pin: Data pin for 1-Wire bus
        """
        ...

    def reset(self, required: bool = False) -> bool:
        """Reset the 1-Wire bus.

        Args:
            required: Raise OSError if no device responds

        Returns:
            True if a device responded with a presence pulse
        """
        ...

    def readbit(self) -> int:
        """Read a single bit."""
        ...

    def readbyte(self) -> int:
        """Read a single byte."""
        ...

    def readinto(self, buf: bytearray) -> None:
        """Read bytes into buffer."""
        ...

    def writebit(self, value: int) -> None:
        """Write a single bit."""
        ...

    def writebyte(self, value: int) -> None:
        """Write a single byte."""
        ...

    def write(self, buf: bytes) -> None:
        """Write bytes to bus."""
        ...

    def select_rom(self, rom: bytes) -> None:
        """Select a specific device by ROM code.

        Args:
            rom: 8-byte ROM code identifying the device
        """
        ...

    def scan(self) -> List[bytearray]:
        """Scan for devices on the bus.

        Returns:
            List of 8-byte ROM codes for found devices
        """
        ...

    def crc8(self, data: bytes) -> int:
        """Calculate CRC8 checksum.

        Args:
            data: Data to checksum

        Returns:
            8-bit CRC value
        """
        ...


class OneWireError(Exception):
    """1-Wire communication error."""
    pass
