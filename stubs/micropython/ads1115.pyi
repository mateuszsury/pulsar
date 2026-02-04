"""Type stubs for ads1115 module (ADS1115 16-bit ADC)."""

from typing import Optional
from machine import I2C

# Gain settings (full-scale range)
GAIN_6_144V: int  # ±6.144V
GAIN_4_096V: int  # ±4.096V
GAIN_2_048V: int  # ±2.048V (default)
GAIN_1_024V: int  # ±1.024V
GAIN_0_512V: int  # ±0.512V
GAIN_0_256V: int  # ±0.256V

# Data rates
RATE_8: int      # 8 samples/second
RATE_16: int     # 16 samples/second
RATE_32: int     # 32 samples/second
RATE_64: int     # 64 samples/second
RATE_128: int    # 128 samples/second (default)
RATE_250: int    # 250 samples/second
RATE_475: int    # 475 samples/second
RATE_860: int    # 860 samples/second


class ADS1115:
    """ADS1115 16-bit 4-channel ADC.

    Example:
        from machine import Pin, I2C
        from ads1115 import ADS1115

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        adc = ADS1115(i2c)

        # Read single-ended (channel 0 vs GND)
        value = adc.read(0)
        print(f"Raw: {value}")

        # Read voltage
        voltage = adc.read_voltage(0)
        print(f"Voltage: {voltage}V")

        # Read differential (A0-A1)
        diff = adc.read_diff(0, 1)
    """

    def __init__(
        self,
        i2c: I2C,
        address: int = 0x48,
        gain: int = GAIN_2_048V
    ) -> None:
        """Create ADS1115 ADC.

        Args:
            i2c: I2C bus object
            address: I2C address (0x48-0x4B depending on ADDR pin)
            gain: Gain setting (GAIN_* constant)
        """
        ...

    def read(self, channel: int) -> int:
        """Read single-ended value from channel.

        Args:
            channel: Channel number (0-3)

        Returns:
            16-bit signed value (-32768 to 32767)
        """
        ...

    def read_diff(self, channel1: int, channel2: int) -> int:
        """Read differential value between two channels.

        Args:
            channel1: Positive channel (0-3)
            channel2: Negative channel (0-3)

        Returns:
            16-bit signed differential value
        """
        ...

    def read_voltage(self, channel: int) -> float:
        """Read voltage from channel.

        Args:
            channel: Channel number (0-3)

        Returns:
            Voltage in volts
        """
        ...

    def read_diff_voltage(self, channel1: int, channel2: int) -> float:
        """Read differential voltage.

        Args:
            channel1: Positive channel
            channel2: Negative channel

        Returns:
            Differential voltage in volts
        """
        ...

    @property
    def gain(self) -> int:
        """Get current gain setting."""
        ...

    @gain.setter
    def gain(self, value: int) -> None:
        """Set gain (GAIN_* constant)."""
        ...

    @property
    def rate(self) -> int:
        """Get current data rate."""
        ...

    @rate.setter
    def rate(self, value: int) -> None:
        """Set data rate (RATE_* constant)."""
        ...

    def alert_start(
        self,
        channel: int,
        threshold_high: int,
        threshold_low: int,
        latched: bool = False
    ) -> None:
        """Start comparator alert mode.

        Args:
            channel: Channel to monitor
            threshold_high: High threshold value
            threshold_low: Low threshold value
            latched: Latch alert until read
        """
        ...

    def alert_read(self) -> bool:
        """Read alert status.

        Returns:
            True if alert is active
        """
        ...


class ADS1015(ADS1115):
    """ADS1015 12-bit 4-channel ADC.

    Same interface as ADS1115 but 12-bit resolution.
    """
    pass
