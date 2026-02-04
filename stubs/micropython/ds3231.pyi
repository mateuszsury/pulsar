"""Type stubs for ds3231 module (DS3231 RTC with temperature sensor)."""

from typing import Tuple
from machine import I2C


class DS3231:
    """DS3231 high-precision RTC with temperature sensor.

    Example:
        from machine import Pin, I2C
        from ds3231 import DS3231

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        rtc = DS3231(i2c)

        # Set time: year, month, day, weekday, hour, minute, second
        rtc.datetime((2026, 1, 15, 1, 12, 30, 0))

        # Read time
        dt = rtc.datetime()
        print(f"{dt[0]}-{dt[1]:02d}-{dt[2]:02d} {dt[4]:02d}:{dt[5]:02d}:{dt[6]:02d}")

        # Read temperature
        print(f"Temperature: {rtc.temperature()}°C")
    """

    def __init__(self, i2c: I2C, addr: int = 0x68) -> None:
        """Create DS3231 RTC interface.

        Args:
            i2c: I2C bus object
            addr: I2C address (default 0x68)
        """
        ...

    def datetime(
        self,
        dt: Tuple[int, int, int, int, int, int, int] = None
    ) -> Tuple[int, int, int, int, int, int, int]:
        """Get or set date/time.

        Args:
            dt: Datetime tuple to set, or None to read

        Tuple format: (year, month, day, weekday, hour, minute, second)
        - year: 2000-2099
        - month: 1-12
        - day: 1-31
        - weekday: 1-7 (1=Monday)
        - hour: 0-23
        - minute: 0-59
        - second: 0-59

        Returns:
            Current datetime tuple
        """
        ...

    def temperature(self) -> float:
        """Read temperature from RTC.

        Returns:
            Temperature in degrees Celsius (0.25°C resolution)
        """
        ...

    def alarm1(
        self,
        time: Tuple[int, int, int, int] = None,
        match: int = 0
    ) -> Tuple[int, int, int, int]:
        """Get or set alarm 1.

        Args:
            time: (day, hour, minute, second) tuple, or None to read
            match: Match mode (0-4)

        Match modes:
            0: Once per second
            1: Match seconds
            2: Match minutes and seconds
            3: Match hours, minutes, seconds
            4: Match day, hours, minutes, seconds

        Returns:
            Current alarm 1 setting
        """
        ...

    def alarm2(
        self,
        time: Tuple[int, int, int] = None,
        match: int = 0
    ) -> Tuple[int, int, int]:
        """Get or set alarm 2.

        Args:
            time: (day, hour, minute) tuple, or None to read
            match: Match mode (0-3)

        Returns:
            Current alarm 2 setting
        """
        ...

    def alarm1_triggered(self) -> bool:
        """Check if alarm 1 has triggered.

        Returns:
            True if alarm triggered
        """
        ...

    def alarm2_triggered(self) -> bool:
        """Check if alarm 2 has triggered.

        Returns:
            True if alarm triggered
        """
        ...

    def clear_alarm1(self) -> None:
        """Clear alarm 1 flag."""
        ...

    def clear_alarm2(self) -> None:
        """Clear alarm 2 flag."""
        ...

    def enable_alarm1_interrupt(self, enable: bool = True) -> None:
        """Enable/disable alarm 1 interrupt output."""
        ...

    def enable_alarm2_interrupt(self, enable: bool = True) -> None:
        """Enable/disable alarm 2 interrupt output."""
        ...

    def square_wave(self, freq: int = None) -> int:
        """Get or set square wave output frequency.

        Args:
            freq: Frequency in Hz (1, 1024, 4096, 8192) or 0 to disable

        Returns:
            Current frequency setting
        """
        ...
