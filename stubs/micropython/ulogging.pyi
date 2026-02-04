"""Type stubs for ulogging module (logging)."""

from typing import Any, Optional

# Log levels
CRITICAL: int  # 50
ERROR: int     # 40
WARNING: int   # 30
INFO: int      # 20
DEBUG: int     # 10
NOTSET: int    # 0


class Logger:
    """Logger object for structured logging."""

    level: int
    name: str

    def __init__(self, name: str) -> None:
        """Create logger.

        Args:
            name: Logger name
        """
        ...

    def setLevel(self, level: int) -> None:
        """Set minimum logging level.

        Args:
            level: CRITICAL, ERROR, WARNING, INFO, DEBUG, or NOTSET
        """
        ...

    def isEnabledFor(self, level: int) -> bool:
        """Check if level is enabled.

        Args:
            level: Log level to check
        """
        ...

    def debug(self, msg: str, *args: Any) -> None:
        """Log debug message.

        Args:
            msg: Message format string
            args: Format arguments
        """
        ...

    def info(self, msg: str, *args: Any) -> None:
        """Log info message."""
        ...

    def warning(self, msg: str, *args: Any) -> None:
        """Log warning message."""
        ...

    def error(self, msg: str, *args: Any) -> None:
        """Log error message."""
        ...

    def critical(self, msg: str, *args: Any) -> None:
        """Log critical message."""
        ...

    def exception(self, msg: str, *args: Any) -> None:
        """Log error with exception info."""
        ...

    def log(self, level: int, msg: str, *args: Any) -> None:
        """Log message at specified level."""
        ...


def getLogger(name: str = None) -> Logger:
    """Get or create a logger.

    Args:
        name: Logger name (None for root logger)

    Returns:
        Logger instance
    """
    ...


def basicConfig(
    level: int = WARNING,
    filename: Optional[str] = None,
    format: Optional[str] = None,
    stream: Any = None
) -> None:
    """Configure basic logging.

    Args:
        level: Minimum log level
        filename: Log to file
        format: Message format string
        stream: Output stream

    Example:
        import ulogging

        ulogging.basicConfig(level=ulogging.DEBUG)
        log = ulogging.getLogger('myapp')
        log.info("Application started")
    """
    ...


# Module-level functions (use root logger)
def debug(msg: str, *args: Any) -> None:
    """Log debug message to root logger."""
    ...


def info(msg: str, *args: Any) -> None:
    """Log info message to root logger."""
    ...


def warning(msg: str, *args: Any) -> None:
    """Log warning message to root logger."""
    ...


def error(msg: str, *args: Any) -> None:
    """Log error message to root logger."""
    ...


def critical(msg: str, *args: Any) -> None:
    """Log critical message to root logger."""
    ...


def exception(msg: str, *args: Any) -> None:
    """Log exception to root logger."""
    ...
