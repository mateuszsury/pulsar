"""Type stubs for MicroPython dht module (DHT11/DHT22 temperature & humidity sensors)."""

from machine import Pin


class DHTBase:
    """Base class for DHT sensors."""

    def __init__(self, pin: Pin) -> None:
        """Create DHT sensor interface.

        Args:
            pin: Data pin connected to sensor
        """
        ...

    def measure(self) -> None:
        """Trigger a measurement.

        Call this before reading temperature/humidity.
        Raises OSError on timeout or checksum error.
        """
        ...

    def temperature(self) -> float:
        """Get temperature in Celsius.

        Returns:
            Temperature in degrees Celsius

        Note:
            Call measure() first to get fresh reading.
        """
        ...

    def humidity(self) -> float:
        """Get relative humidity.

        Returns:
            Relative humidity in percent (0-100)

        Note:
            Call measure() first to get fresh reading.
        """
        ...


class DHT11(DHTBase):
    """DHT11 temperature and humidity sensor.

    Specifications:
        - Temperature: 0-50°C, ±2°C accuracy
        - Humidity: 20-80%, ±5% accuracy
        - Sampling rate: 1Hz (once per second)

    Example:
        from machine import Pin
        import dht

        sensor = dht.DHT11(Pin(4))
        sensor.measure()
        print(f"Temperature: {sensor.temperature()}°C")
        print(f"Humidity: {sensor.humidity()}%")
    """
    pass


class DHT22(DHTBase):
    """DHT22 (AM2302) temperature and humidity sensor.

    Specifications:
        - Temperature: -40-80°C, ±0.5°C accuracy
        - Humidity: 0-100%, ±2% accuracy
        - Sampling rate: 0.5Hz (once per 2 seconds)

    Example:
        from machine import Pin
        import dht

        sensor = dht.DHT22(Pin(4))
        sensor.measure()
        print(f"Temperature: {sensor.temperature()}°C")
        print(f"Humidity: {sensor.humidity()}%")
    """
    pass
