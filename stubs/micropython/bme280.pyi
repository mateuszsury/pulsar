"""Type stubs for bme280 module (BME280 environmental sensor)."""

from typing import Optional, Tuple
from machine import I2C

# Oversampling settings
BME280_OSAMPLE_1: int
BME280_OSAMPLE_2: int
BME280_OSAMPLE_4: int
BME280_OSAMPLE_8: int
BME280_OSAMPLE_16: int


class BME280:
    """BME280 temperature, humidity, and pressure sensor.

    Example:
        from machine import Pin, I2C
        from bme280 import BME280

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        bme = BME280(i2c=i2c)

        print(bme.values)  # ('25.00C', '1013.25hPa', '45.00%')
        print(bme.temperature)  # 25.0 (float)
    """

    def __init__(
        self,
        mode: int = BME280_OSAMPLE_1,
        address: int = 0x76,
        i2c: Optional[I2C] = None,
        **kwargs
    ) -> None:
        """Create BME280 sensor.

        Args:
            mode: Oversampling mode
            address: I2C address (0x76 or 0x77)
            i2c: I2C bus object
        """
        ...

    @property
    def temperature(self) -> float:
        """Temperature in degrees Celsius."""
        ...

    @property
    def pressure(self) -> float:
        """Pressure in hPa (hectopascals)."""
        ...

    @property
    def humidity(self) -> float:
        """Relative humidity in percent."""
        ...

    @property
    def values(self) -> Tuple[str, str, str]:
        """Formatted sensor values.

        Returns:
            Tuple of (temperature, pressure, humidity) as strings
            Example: ('25.00C', '1013.25hPa', '45.00%')
        """
        ...

    def read_compensated_data(self) -> Tuple[float, float, float]:
        """Read compensated sensor data.

        Returns:
            Tuple of (temperature, pressure, humidity) as floats
        """
        ...

    def read_raw_data(self) -> Tuple[int, int, int]:
        """Read raw sensor data.

        Returns:
            Tuple of (temperature, pressure, humidity) as raw ADC values
        """
        ...

    @property
    def sealevel(self) -> float:
        """Sea level pressure for altitude calculation."""
        ...

    @sealevel.setter
    def sealevel(self, value: float) -> None:
        """Set sea level pressure.

        Args:
            value: Sea level pressure in hPa
        """
        ...

    @property
    def altitude(self) -> float:
        """Calculated altitude in meters.

        Based on current pressure and sealevel setting.
        """
        ...

    @property
    def dew_point(self) -> float:
        """Calculated dew point in degrees Celsius."""
        ...


class BMP280(BME280):
    """BMP280 temperature and pressure sensor (no humidity).

    Same interface as BME280 but humidity always returns 0.
    """
    pass
