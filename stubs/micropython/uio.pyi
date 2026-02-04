"""Type stubs for MicroPython uio module (I/O streams)."""

from typing import Any, Optional, Union


class FileIO:
    """Raw file I/O.

    Example:
        f = uio.FileIO('/data.bin', 'rb')
        data = f.read()
        f.close()
    """

    def __init__(self, name: str, mode: str = 'r') -> None:
        """Open file.

        Args:
            name: File path
            mode: Open mode ('r', 'w', 'rb', 'wb', etc.)
        """
        ...

    def read(self, size: int = -1) -> bytes:
        """Read bytes from file."""
        ...

    def readinto(self, buf: bytearray) -> int:
        """Read into buffer."""
        ...

    def readline(self) -> bytes:
        """Read one line."""
        ...

    def readlines(self) -> list:
        """Read all lines."""
        ...

    def write(self, data: bytes) -> int:
        """Write bytes to file."""
        ...

    def seek(self, offset: int, whence: int = 0) -> int:
        """Seek to position.

        Args:
            offset: Byte offset
            whence: 0=start, 1=current, 2=end
        """
        ...

    def tell(self) -> int:
        """Return current position."""
        ...

    def flush(self) -> None:
        """Flush write buffers."""
        ...

    def close(self) -> None:
        """Close file."""
        ...

    def __enter__(self) -> "FileIO":
        ...

    def __exit__(self, *args: Any) -> None:
        ...


class TextIOWrapper:
    """Text mode file wrapper."""

    def __init__(self, stream: Any, encoding: str = 'utf-8') -> None:
        """Wrap binary stream for text I/O.

        Args:
            stream: Binary stream
            encoding: Text encoding
        """
        ...

    def read(self, size: int = -1) -> str:
        """Read text."""
        ...

    def readline(self) -> str:
        """Read one line."""
        ...

    def readlines(self) -> list:
        """Read all lines."""
        ...

    def write(self, data: str) -> int:
        """Write text."""
        ...

    def close(self) -> None:
        """Close stream."""
        ...

    def __enter__(self) -> "TextIOWrapper":
        ...

    def __exit__(self, *args: Any) -> None:
        ...


class StringIO:
    """In-memory text stream.

    Example:
        s = uio.StringIO()
        s.write('Hello ')
        s.write('World')
        print(s.getvalue())  # 'Hello World'
    """

    def __init__(self, string: str = '') -> None:
        """Create StringIO.

        Args:
            string: Initial content
        """
        ...

    def read(self, size: int = -1) -> str:
        """Read from buffer."""
        ...

    def readline(self) -> str:
        """Read one line."""
        ...

    def write(self, s: str) -> int:
        """Write to buffer."""
        ...

    def getvalue(self) -> str:
        """Return entire buffer content."""
        ...

    def seek(self, offset: int, whence: int = 0) -> int:
        """Seek to position."""
        ...

    def tell(self) -> int:
        """Return current position."""
        ...

    def close(self) -> None:
        """Close (no-op, but frees buffer)."""
        ...


class BytesIO:
    """In-memory binary stream.

    Example:
        b = uio.BytesIO()
        b.write(b'Hello')
        print(b.getvalue())  # b'Hello'
    """

    def __init__(self, data: bytes = b'') -> None:
        """Create BytesIO.

        Args:
            data: Initial content
        """
        ...

    def read(self, size: int = -1) -> bytes:
        """Read from buffer."""
        ...

    def readinto(self, buf: bytearray) -> int:
        """Read into buffer."""
        ...

    def readline(self) -> bytes:
        """Read one line."""
        ...

    def write(self, data: bytes) -> int:
        """Write to buffer."""
        ...

    def getvalue(self) -> bytes:
        """Return entire buffer content."""
        ...

    def seek(self, offset: int, whence: int = 0) -> int:
        """Seek to position."""
        ...

    def tell(self) -> int:
        """Return current position."""
        ...

    def close(self) -> None:
        """Close (no-op, but frees buffer)."""
        ...


def open(
    name: str,
    mode: str = 'r',
    buffering: int = -1,
    encoding: Optional[str] = None
) -> Union[FileIO, TextIOWrapper]:
    """Open a file.

    Args:
        name: File path
        mode: Open mode
        buffering: Buffer size
        encoding: Text encoding

    Returns:
        File object
    """
    ...
