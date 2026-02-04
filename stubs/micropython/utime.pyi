"""Type stubs for MicroPython utime module (time functions)."""

from typing import Optional, Tuple

def gmtime(secs: Optional[int] = None) -> Tuple[int, int, int, int, int, int, int, int]:
    """Convert time to UTC tuple.

    Args:
        secs: Seconds since epoch (None for current time)

    Returns:
        Tuple of (year, month, mday, hour, minute, second, weekday, yearday)
    """
    ...

def localtime(secs: Optional[int] = None) -> Tuple[int, int, int, int, int, int, int, int]:
    """Convert time to local time tuple.

    Args:
        secs: Seconds since epoch (None for current time)

    Returns:
        Tuple of (year, month, mday, hour, minute, second, weekday, yearday)
    """
    ...

def mktime(t: Tuple[int, int, int, int, int, int, int, int]) -> int:
    """Convert time tuple to seconds since epoch.

    Args:
        t: Time tuple (year, month, mday, hour, minute, second, weekday, yearday)

    Returns:
        Seconds since epoch
    """
    ...

def time() -> int:
    """Get current time in seconds since epoch.

    Returns:
        Seconds since Jan 1, 2000 (MicroPython epoch)
    """
    ...

def time_ns() -> int:
    """Get current time in nanoseconds.

    Returns:
        Nanoseconds since epoch
    """
    ...

def sleep(seconds: float) -> None:
    """Sleep for a number of seconds.

    Args:
        seconds: Sleep duration (can be float)
    """
    ...

def sleep_ms(ms: int) -> None:
    """Sleep for a number of milliseconds.

    Args:
        ms: Sleep duration in milliseconds
    """
    ...

def sleep_us(us: int) -> None:
    """Sleep for a number of microseconds.

    Args:
        us: Sleep duration in microseconds
    """
    ...

def ticks_ms() -> int:
    """Get millisecond counter (wraps around).

    Returns:
        Millisecond tick counter
    """
    ...

def ticks_us() -> int:
    """Get microsecond counter (wraps around).

    Returns:
        Microsecond tick counter
    """
    ...

def ticks_cpu() -> int:
    """Get CPU tick counter (highest resolution).

    Returns:
        CPU tick counter
    """
    ...

def ticks_add(ticks: int, delta: int) -> int:
    """Add delta to a tick value (handles wrap).

    Args:
        ticks: Tick value from ticks_ms/us/cpu
        delta: Delta to add (can be negative)

    Returns:
        New tick value
    """
    ...

def ticks_diff(ticks1: int, ticks2: int) -> int:
    """Compute difference between tick values (handles wrap).

    Args:
        ticks1: Later tick value
        ticks2: Earlier tick value

    Returns:
        ticks1 - ticks2 (signed, handles wrap-around)
    """
    ...
