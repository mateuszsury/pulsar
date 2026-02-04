"""Type stubs for MicroPython micropython module (MicroPython internals)."""

from typing import Any, Callable, Optional, TypeVar

_T = TypeVar("_T")

def const(value: _T) -> _T:
    """Declare a value as a compile-time constant.

    Used for optimization in MicroPython.

    Args:
        value: The constant value

    Returns:
        The same value (at compile time, enables optimization)
    """
    ...

def opt_level(level: Optional[int] = None) -> Optional[int]:
    """Get or set the optimization level.

    Args:
        level: 0 (none), 1 (remove assert), 2 (also remove docstrings)

    Returns:
        Current level if level is None
    """
    ...

def alloc_emergency_exception_buf(size: int) -> None:
    """Allocate buffer for exceptions in ISRs.

    Should be called early in boot.py.

    Args:
        size: Buffer size in bytes (100 recommended)
    """
    ...

def mem_info(verbose: bool = False) -> None:
    """Print memory usage information.

    Args:
        verbose: If True, print detailed memory map
    """
    ...

def qstr_info(verbose: bool = False) -> None:
    """Print interned string (qstr) information.

    Args:
        verbose: If True, print all interned strings
    """
    ...

def stack_use() -> int:
    """Get current stack usage.

    Returns:
        Bytes of stack used
    """
    ...

def heap_lock() -> None:
    """Lock the heap to prevent allocation.

    Useful for time-critical code.
    """
    ...

def heap_unlock() -> None:
    """Unlock the heap to allow allocation."""
    ...

def heap_locked() -> bool:
    """Check if heap is locked.

    Returns:
        True if heap is locked
    """
    ...

def kbd_intr(chr: int) -> None:
    """Set the character for keyboard interrupt.

    Args:
        chr: Character code (-1 to disable)
    """
    ...

def schedule(func: Callable[..., Any], arg: Any) -> None:
    """Schedule a function to be called from main context.

    Can be called from interrupt handlers.

    Args:
        func: Function to call
        arg: Argument to pass to function
    """
    ...

class RingIO:
    """Ring buffer for inter-thread/ISR communication."""

    def __init__(self, size: int) -> None:
        """Create a ring buffer.

        Args:
            size: Buffer size in bytes
        """
        ...

    def any(self) -> int:
        """Return number of bytes available to read."""
        ...

    def read(self, nbytes: Optional[int] = None) -> bytes:
        """Read bytes from buffer."""
        ...

    def readline(self) -> bytes:
        """Read a line from buffer."""
        ...

    def readinto(self, buf: bytearray) -> int:
        """Read into a buffer."""
        ...

    def write(self, buf: bytes) -> int:
        """Write bytes to buffer."""
        ...
