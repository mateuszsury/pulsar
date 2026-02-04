"""Type stubs for pca9685 module (PCA9685 16-channel PWM driver)."""

from machine import I2C


class PCA9685:
    """PCA9685 16-channel 12-bit PWM driver.

    Used for controlling servos, LEDs, and other PWM devices.

    Example:
        from machine import Pin, I2C
        from pca9685 import PCA9685

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        pca = PCA9685(i2c)
        pca.freq(50)  # 50Hz for servos

        # Set channel 0 duty cycle
        pca.duty(0, 1500)  # ~1.5ms pulse (servo center)
    """

    def __init__(self, i2c: I2C, address: int = 0x40) -> None:
        """Create PCA9685 driver.

        Args:
            i2c: I2C bus object
            address: I2C address (default 0x40)
        """
        ...

    def reset(self) -> None:
        """Reset the PCA9685."""
        ...

    def freq(self, freq: int = None) -> int:
        """Get or set PWM frequency.

        Args:
            freq: Frequency in Hz (24-1526), or None to read

        Returns:
            Current frequency
        """
        ...

    def pwm(self, index: int, on: int = None, off: int = None) -> tuple:
        """Get or set raw PWM values for a channel.

        Args:
            index: Channel number (0-15)
            on: Start tick (0-4095)
            off: End tick (0-4095)

        Returns:
            Tuple of (on, off) values
        """
        ...

    def duty(self, index: int, value: int = None, invert: bool = False) -> int:
        """Get or set duty cycle for a channel.

        Args:
            index: Channel number (0-15)
            value: Duty cycle (0-4095), or None to read
            invert: Invert the signal

        Returns:
            Current duty cycle value
        """
        ...


class Servo:
    """Servo motor control using PCA9685.

    Example:
        from machine import Pin, I2C
        from pca9685 import PCA9685, Servo

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        pca = PCA9685(i2c)
        pca.freq(50)

        servo = Servo(pca, 0)  # Servo on channel 0
        servo.angle(90)  # Move to 90 degrees
    """

    def __init__(
        self,
        pca9685: PCA9685,
        index: int,
        min_us: int = 600,
        max_us: int = 2400,
        degrees: int = 180
    ) -> None:
        """Create servo controller.

        Args:
            pca9685: PCA9685 driver instance
            index: Channel number (0-15)
            min_us: Minimum pulse width in microseconds
            max_us: Maximum pulse width in microseconds
            degrees: Total range of motion in degrees
        """
        ...

    def angle(self, degrees: int = None) -> int:
        """Get or set servo angle.

        Args:
            degrees: Target angle (0 to max_degrees), or None to read

        Returns:
            Current angle
        """
        ...

    def release(self) -> None:
        """Release the servo (stop sending PWM signal)."""
        ...


class Motor:
    """DC motor control using PCA9685.

    Example:
        from machine import Pin, I2C
        from pca9685 import PCA9685, Motor

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        pca = PCA9685(i2c)

        motor = Motor(pca, 0, 1)  # Using channels 0 and 1
        motor.speed(100)  # Full forward
        motor.speed(-50)  # Half reverse
        motor.brake()  # Stop
    """

    def __init__(self, pca9685: PCA9685, pin1: int, pin2: int) -> None:
        """Create motor controller.

        Args:
            pca9685: PCA9685 driver instance
            pin1: First channel number (forward)
            pin2: Second channel number (reverse)
        """
        ...

    def speed(self, value: int = None) -> int:
        """Get or set motor speed.

        Args:
            value: Speed (-100 to 100), or None to read

        Returns:
            Current speed
        """
        ...

    def brake(self) -> None:
        """Stop the motor immediately."""
        ...
