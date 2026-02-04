"""Type stubs for mpu6050 module (MPU6050 accelerometer/gyroscope)."""

from typing import Tuple
from machine import I2C


class MPU6050:
    """MPU6050 6-axis accelerometer and gyroscope.

    Example:
        from machine import Pin, I2C
        from mpu6050 import MPU6050

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        mpu = MPU6050(i2c)

        print(mpu.acceleration)  # (ax, ay, az) in g
        print(mpu.gyro)  # (gx, gy, gz) in degrees/s
        print(mpu.temperature)  # Temperature in Celsius
    """

    # Accelerometer range constants
    ACCEL_RANGE_2G: int
    ACCEL_RANGE_4G: int
    ACCEL_RANGE_8G: int
    ACCEL_RANGE_16G: int

    # Gyroscope range constants
    GYRO_RANGE_250DEG: int
    GYRO_RANGE_500DEG: int
    GYRO_RANGE_1000DEG: int
    GYRO_RANGE_2000DEG: int

    # Filter bandwidth constants
    FILTER_BW_256: int
    FILTER_BW_188: int
    FILTER_BW_98: int
    FILTER_BW_42: int
    FILTER_BW_20: int
    FILTER_BW_10: int
    FILTER_BW_5: int

    def __init__(self, i2c: I2C, addr: int = 0x68) -> None:
        """Create MPU6050 interface.

        Args:
            i2c: I2C bus object
            addr: I2C address (0x68 or 0x69)
        """
        ...

    def wake(self) -> None:
        """Wake sensor from sleep mode."""
        ...

    def sleep(self) -> None:
        """Put sensor in sleep mode."""
        ...

    @property
    def temperature(self) -> float:
        """Temperature in degrees Celsius."""
        ...

    @property
    def acceleration(self) -> Tuple[float, float, float]:
        """Acceleration in g (x, y, z).

        Returns:
            Tuple of (ax, ay, az) in units of g (9.8 m/s²)
        """
        ...

    @property
    def gyro(self) -> Tuple[float, float, float]:
        """Angular velocity in degrees/second (x, y, z).

        Returns:
            Tuple of (gx, gy, gz) in degrees per second
        """
        ...

    def get_accel_range(self) -> int:
        """Get accelerometer range setting."""
        ...

    def set_accel_range(self, accel_range: int) -> None:
        """Set accelerometer range.

        Args:
            accel_range: ACCEL_RANGE_2G/4G/8G/16G
        """
        ...

    def get_gyro_range(self) -> int:
        """Get gyroscope range setting."""
        ...

    def set_gyro_range(self, gyro_range: int) -> None:
        """Set gyroscope range.

        Args:
            gyro_range: GYRO_RANGE_250/500/1000/2000DEG
        """
        ...

    def get_filter_range(self) -> int:
        """Get digital low-pass filter bandwidth."""
        ...

    def set_filter_range(self, filter_range: int) -> None:
        """Set digital low-pass filter bandwidth.

        Args:
            filter_range: FILTER_BW_* constant
        """
        ...

    def read_raw_data(self) -> Tuple[int, int, int, int, int, int, int]:
        """Read raw sensor data.

        Returns:
            Tuple of (ax, ay, az, temp, gx, gy, gz) as raw 16-bit values
        """
        ...
