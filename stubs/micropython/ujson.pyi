"""Type stubs for MicroPython ujson module (JSON encoding/decoding)."""

from typing import Any, IO, Optional

def dumps(obj: Any, separators: Optional[tuple[str, str]] = None) -> str:
    """Convert object to JSON string.

    Args:
        obj: Object to serialize
        separators: Tuple of (item_separator, key_separator)

    Returns:
        JSON string
    """
    ...

def dump(obj: Any, stream: IO[str], separators: Optional[tuple[str, str]] = None) -> None:
    """Write object as JSON to a stream.

    Args:
        obj: Object to serialize
        stream: File-like object to write to
        separators: Tuple of (item_separator, key_separator)
    """
    ...

def loads(s: str) -> Any:
    """Parse JSON string to object.

    Args:
        s: JSON string

    Returns:
        Parsed object
    """
    ...

def load(stream: IO[str]) -> Any:
    """Parse JSON from a stream.

    Args:
        stream: File-like object to read from

    Returns:
        Parsed object
    """
    ...
