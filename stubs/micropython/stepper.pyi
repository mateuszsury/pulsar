"""Type stubs for stepper module (stepper motor control)."""

from typing import Optional
from machine import Pin


class Stepper:
    """Stepper motor driver.

    Supports common stepper motor drivers like A4988, DRV8825, ULN2003.

    Example:
        from machine import Pin
        from stepper import Stepper

        # For A4988/DRV8825 driver
        motor = Stepper(step_pin=Pin(18), dir_pin=Pin(19))
        motor.steps_per_rev = 200  # NEMA 17

        motor.step(100)  # Move 100 steps forward
        motor.step(-50)  # Move 50 steps backward

        # Or for ULN2003 driver (4-pin)
        motor = Stepper(pins=[Pin(18), Pin(19), Pin(21), Pin(22)])
    """

    def __init__(
        self,
        step_pin: Optional[Pin] = None,
        dir_pin: Optional[Pin] = None,
        enable_pin: Optional[Pin] = None,
        pins: Optional[list] = None,
        steps_per_rev: int = 200,
        delay_us: int = 2000
    ) -> None:
        """Create stepper motor driver.

        For A4988/DRV8825 (2-pin mode):
            step_pin: Step pulse pin
            dir_pin: Direction pin
            enable_pin: Optional enable pin

        For ULN2003/4-pin mode:
            pins: List of 4 GPIO pins [IN1, IN2, IN3, IN4]

        Args:
            steps_per_rev: Steps per revolution (200 for 1.8° motor)
            delay_us: Delay between steps in microseconds
        """
        ...

    @property
    def steps_per_rev(self) -> int:
        """Steps per revolution."""
        ...

    @steps_per_rev.setter
    def steps_per_rev(self, value: int) -> None:
        ...

    @property
    def delay_us(self) -> int:
        """Delay between steps in microseconds."""
        ...

    @delay_us.setter
    def delay_us(self, value: int) -> None:
        ...

    def enable(self) -> None:
        """Enable the motor driver."""
        ...

    def disable(self) -> None:
        """Disable the motor driver (motor can freewheel)."""
        ...

    def step(self, steps: int) -> None:
        """Move specified number of steps.

        Args:
            steps: Number of steps (positive=forward, negative=backward)
        """
        ...

    def step_until(self, condition: callable, direction: int = 1) -> int:
        """Step until condition is met.

        Args:
            condition: Function that returns True to stop
            direction: 1=forward, -1=backward

        Returns:
            Number of steps taken
        """
        ...

    def angle(self, degrees: float) -> None:
        """Rotate by specified angle.

        Args:
            degrees: Angle in degrees (positive=clockwise)
        """
        ...

    def revolution(self, revolutions: float = 1.0) -> None:
        """Rotate specified number of revolutions.

        Args:
            revolutions: Number of full rotations
        """
        ...

    def set_speed(self, rpm: float) -> None:
        """Set rotation speed.

        Args:
            rpm: Speed in revolutions per minute
        """
        ...

    def stop(self) -> None:
        """Stop the motor immediately."""
        ...


class AccelStepper(Stepper):
    """Stepper motor with acceleration control.

    Example:
        from machine import Pin
        from stepper import AccelStepper

        motor = AccelStepper(step_pin=Pin(18), dir_pin=Pin(19))
        motor.set_acceleration(1000)  # steps/sec²
        motor.set_max_speed(2000)  # steps/sec

        motor.move_to(1000)  # Move to position 1000
        while motor.is_running():
            motor.run()
    """

    def __init__(
        self,
        step_pin: Optional[Pin] = None,
        dir_pin: Optional[Pin] = None,
        enable_pin: Optional[Pin] = None,
        pins: Optional[list] = None,
        steps_per_rev: int = 200
    ) -> None:
        ...

    def set_max_speed(self, speed: float) -> None:
        """Set maximum speed in steps/second."""
        ...

    def set_acceleration(self, accel: float) -> None:
        """Set acceleration in steps/second²."""
        ...

    def set_current_position(self, position: int) -> None:
        """Set current position (resets to this position)."""
        ...

    def current_position(self) -> int:
        """Get current position in steps."""
        ...

    def target_position(self) -> int:
        """Get target position in steps."""
        ...

    def distance_to_go(self) -> int:
        """Get remaining distance to target."""
        ...

    def move(self, relative: int) -> None:
        """Set target position relative to current.

        Args:
            relative: Steps to move (positive or negative)
        """
        ...

    def move_to(self, absolute: int) -> None:
        """Set absolute target position.

        Args:
            absolute: Target position in steps
        """
        ...

    def run(self) -> bool:
        """Run one step if needed (call in loop).

        Returns:
            True if motor is still running
        """
        ...

    def run_to_position(self) -> None:
        """Run to target position (blocking)."""
        ...

    def run_speed(self) -> bool:
        """Run at constant speed (no acceleration).

        Returns:
            True if a step was taken
        """
        ...

    def is_running(self) -> bool:
        """Check if motor is still moving."""
        ...

    def stop(self) -> None:
        """Stop with deceleration."""
        ...
