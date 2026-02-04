"""Type stubs for ahtx0 module (AHT10/AHT20 temperature & humidity sensors)."""

from machine import I2C


class AHT10:
    """AHT10 temperature and humidity sensor.

    Example:
        from machine import Pin, I2C
        from ahtx0 import AHT10

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        sensor = AHT10(i2c)

        print(f"Temperature: {sensor.temperature}°C")
        print(f"Humidity: {sensor.relative_humidity}%")
    """

    def __init__(self, i2c: I2C, address: int = 0x38) -> None:
        """Create AHT10 sensor.

        Args:
            i2c: I2C bus object
            address: I2C address (default 0x38)
        """
        ...

    @property
    def temperature(self) -> float:
        """Temperature in degrees Celsius."""
        ...

    @property
    def relative_humidity(self) -> float:
        """Relative humidity in percent (0-100)."""
        ...

    def reset(self) -> None:
        """Soft reset the sensor."""
        ...

    def calibrate(self) -> bool:
        """Calibrate the sensor.

        Returns:
            True if calibration successful
        """
        ...

    @property
    def is_calibrated(self) -> bool:
        """Check if sensor is calibrated."""
        ...


class AHT20(AHT10):
    """AHT20 temperature and humidity sensor.

    Improved version of AHT10 with better accuracy.
    Same interface as AHT10.

    Specifications:
        - Temperature: -40 to 85°C, ±0.3°C accuracy
        - Humidity: 0-100%, ±2% accuracy
    """
    pass
