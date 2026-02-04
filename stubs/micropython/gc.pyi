"""Type stubs for MicroPython gc module (garbage collection)."""

from typing import Optional

def enable() -> None:
    """Enable automatic garbage collection."""
    ...

def disable() -> None:
    """Disable automatic garbage collection."""
    ...

def isenabled() -> bool:
    """Check if automatic GC is enabled.

    Returns:
        True if automatic GC is enabled
    """
    ...

def collect() -> int:
    """Run a garbage collection.

    Returns:
        Amount of memory reclaimed (may not be accurate)
    """
    ...

def mem_alloc() -> int:
    """Return the number of bytes of heap RAM that are allocated.

    Returns:
        Bytes of allocated heap memory
    """
    ...

def mem_free() -> int:
    """Return the number of bytes of available heap RAM.

    Returns:
        Bytes of free heap memory
    """
    ...

def threshold(amount: Optional[int] = None) -> Optional[int]:
    """Get or set the GC allocation threshold.

    Args:
        amount: New threshold in bytes (None to query)

    Returns:
        Current threshold if amount is None
    """
    ...
