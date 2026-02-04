"""Type stubs for hcsr04 module (HC-SR04 ultrasonic distance sensor)."""

from machine import Pin


class HCSR04:
    """HC-SR04 ultrasonic distance sensor.

    Measures distance using ultrasonic pulses.
    Range: 2cm to 400cm.

    Example:
        from hcsr04 import HCSR04

        sensor = HCSR04(trigger_pin=5, echo_pin=4)
        distance = sensor.distance_cm()
        print(f"Distance: {distance} cm")
    """

    def __init__(
        self,
        trigger_pin: int,
        echo_pin: int,
        echo_timeout_us: int = 500000
    ) -> None:
        """Create HC-SR04 sensor.

        Args:
            trigger_pin: GPIO pin number for trigger
            echo_pin: GPIO pin number for echo
            echo_timeout_us: Echo timeout in microseconds (default 500ms)
        """
        ...

    def distance_mm(self) -> float:
        """Measure distance in millimeters.

        Returns:
            Distance in mm, or -1 if no echo received
        """
        ...

    def distance_cm(self) -> float:
        """Measure distance in centimeters.

        Returns:
            Distance in cm, or -1 if no echo received
        """
        ...

    def distance_m(self) -> float:
        """Measure distance in meters.

        Returns:
            Distance in meters, or -1 if no echo received
        """
        ...

    def _send_pulse_and_wait(self) -> int:
        """Send ultrasonic pulse and measure echo time.

        Returns:
            Echo time in microseconds
        """
        ...
