"""Type stubs for MicroPython ds18x20 module (DS18B20 temperature sensors)."""

from typing import List, Optional
from onewire import OneWire


class DS18X20:
    """DS18B20/DS18S20 1-Wire temperature sensor driver.

    Example:
        from machine import Pin
        import onewire
        import ds18x20
        import time

        ow = onewire.OneWire(Pin(4))
        ds = ds18x20.DS18X20(ow)

        roms = ds.scan()
        print(f"Found {len(roms)} sensors")

        ds.convert_temp()
        time.sleep_ms(750)  # Wait for conversion

        for rom in roms:
            print(f"Temperature: {ds.read_temp(rom)}°C")
    """

    def __init__(self, onewire: OneWire) -> None:
        """Create DS18X20 driver.

        Args:
            onewire: OneWire bus interface
        """
        ...

    def scan(self) -> List[bytearray]:
        """Scan for DS18x20 sensors on the bus.

        Returns:
            List of ROM codes for found DS18x20 sensors
        """
        ...

    def convert_temp(self) -> None:
        """Start temperature conversion on all sensors.

        Wait at least 750ms before reading temperature (12-bit resolution).
        """
        ...

    def read_temp(self, rom: bytes) -> float:
        """Read temperature from a specific sensor.

        Args:
            rom: 8-byte ROM code of the sensor

        Returns:
            Temperature in degrees Celsius

        Note:
            Call convert_temp() and wait 750ms before reading.
        """
        ...

    def read_scratch(self, rom: bytes) -> bytes:
        """Read scratchpad memory from sensor.

        Args:
            rom: 8-byte ROM code

        Returns:
            9-byte scratchpad contents
        """
        ...

    def write_scratch(self, rom: bytes, buf: bytes) -> None:
        """Write to scratchpad memory.

        Args:
            rom: 8-byte ROM code
            buf: 3 bytes (TH, TL, config register)
        """
        ...

    def resolution(self, rom: bytes, bits: Optional[int] = None) -> int:
        """Get or set temperature resolution.

        Args:
            rom: 8-byte ROM code
            bits: Resolution in bits (9, 10, 11, or 12). None to query.

        Returns:
            Current resolution in bits

        Note:
            Higher resolution = longer conversion time:
            - 9 bits: 93.75ms
            - 10 bits: 187.5ms
            - 11 bits: 375ms
            - 12 bits: 750ms (default)
        """
        ...
