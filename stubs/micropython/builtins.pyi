"""Type stubs for MicroPython built-in additions.

These are MicroPython-specific additions to Python's builtins.
"""

from typing import Any, TypeVar

T = TypeVar('T')


def const(value: T) -> T:
    """Declare a constant value for optimization.

    MicroPython compiler optimizes const() values.

    Example:
        LED_PIN = const(2)
        MAX_VALUE = const(255)

    Args:
        value: Constant value (must be integer)

    Returns:
        The same value
    """
    ...


class memoryview:
    """Memory view object for efficient buffer access.

    MicroPython extends memoryview with additional methods.
    """

    def __init__(self, obj: Any) -> None:
        """Create memoryview.

        Args:
            obj: Object with buffer protocol (bytes, bytearray, etc.)
        """
        ...

    def __len__(self) -> int:
        """Return length."""
        ...

    def __getitem__(self, key: Any) -> Any:
        """Get item or slice."""
        ...

    def __setitem__(self, key: Any, value: Any) -> None:
        """Set item or slice."""
        ...

    @property
    def itemsize(self) -> int:
        """Size of each item in bytes."""
        ...

    @property
    def nbytes(self) -> int:
        """Total size in bytes."""
        ...

    @property
    def format(self) -> str:
        """Format string."""
        ...

    @property
    def shape(self) -> tuple:
        """Shape tuple."""
        ...


# MicroPython has a smaller set of exceptions
class OSError(Exception):
    """Operating system error.

    MicroPython combines many standard Python exceptions into OSError.
    errno attribute contains the error code.
    """

    errno: int
    args: tuple

    def __init__(self, errno: int = 0, msg: str = "") -> None:
        ...


# Aliases for MicroPython compatibility
IOError = OSError
EnvironmentError = OSError
