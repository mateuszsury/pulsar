"""Type stubs for MicroPython ustruct module (binary data packing/unpacking)."""

from typing import Any, Tuple


def calcsize(fmt: str) -> int:
    """Calculate size of packed data.

    Args:
        fmt: Format string

    Returns:
        Size in bytes

    Format characters:
        x - pad byte
        b - signed char (1 byte)
        B - unsigned char (1 byte)
        h - signed short (2 bytes)
        H - unsigned short (2 bytes)
        i - signed int (4 bytes)
        I - unsigned int (4 bytes)
        l - signed long (4 bytes)
        L - unsigned long (4 bytes)
        q - signed long long (8 bytes)
        Q - unsigned long long (8 bytes)
        f - float (4 bytes)
        d - double (8 bytes)
        s - char[] (string)
        P - pointer

    Byte order prefixes:
        @ - native byte order (default)
        = - native byte order, standard size
        < - little-endian
        > - big-endian
        ! - network (big-endian)
    """
    ...


def pack(fmt: str, *values: Any) -> bytes:
    """Pack values into bytes.

    Args:
        fmt: Format string
        values: Values to pack

    Returns:
        Packed bytes

    Example:
        ustruct.pack('<HH', 1, 2)  # Pack two little-endian unsigned shorts
    """
    ...


def pack_into(fmt: str, buffer: bytearray, offset: int, *values: Any) -> None:
    """Pack values into buffer at offset.

    Args:
        fmt: Format string
        buffer: Target buffer
        offset: Byte offset in buffer
        values: Values to pack
    """
    ...


def unpack(fmt: str, data: bytes) -> Tuple[Any, ...]:
    """Unpack bytes into values.

    Args:
        fmt: Format string
        data: Packed bytes

    Returns:
        Tuple of unpacked values

    Example:
        ustruct.unpack('<HH', b'\\x01\\x00\\x02\\x00')  # Returns (1, 2)
    """
    ...


def unpack_from(fmt: str, data: bytes, offset: int = 0) -> Tuple[Any, ...]:
    """Unpack bytes from offset.

    Args:
        fmt: Format string
        data: Packed bytes
        offset: Starting byte offset

    Returns:
        Tuple of unpacked values
    """
    ...
