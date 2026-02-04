"""Type stubs for MicroPython ubinascii module (binary/ASCII conversions)."""

from typing import Union


def hexlify(data: bytes, sep: Union[str, bytes] = ...) -> bytes:
    """Convert bytes to hexadecimal representation.

    Args:
        data: Binary data
        sep: Optional separator between bytes

    Returns:
        Hex string as bytes

    Example:
        ubinascii.hexlify(b'\\xde\\xad')  # Returns b'dead'
        ubinascii.hexlify(b'\\xde\\xad', ':')  # Returns b'de:ad'
    """
    ...


def unhexlify(data: Union[str, bytes]) -> bytes:
    """Convert hexadecimal string to bytes.

    Args:
        data: Hex string (str or bytes)

    Returns:
        Binary data

    Example:
        ubinascii.unhexlify('dead')  # Returns b'\\xde\\xad'
    """
    ...


def a2b_base64(data: Union[str, bytes]) -> bytes:
    """Decode base64 data.

    Args:
        data: Base64-encoded string

    Returns:
        Decoded bytes

    Example:
        ubinascii.a2b_base64('SGVsbG8=')  # Returns b'Hello'
    """
    ...


def b2a_base64(data: bytes, newline: bool = True) -> bytes:
    """Encode bytes as base64.

    Args:
        data: Binary data to encode
        newline: Append newline at end

    Returns:
        Base64-encoded bytes

    Example:
        ubinascii.b2a_base64(b'Hello')  # Returns b'SGVsbG8=\\n'
    """
    ...


def crc32(data: bytes, value: int = 0) -> int:
    """Calculate CRC32 checksum.

    Args:
        data: Data to checksum
        value: Initial CRC value (for incremental calculation)

    Returns:
        32-bit CRC value

    Example:
        ubinascii.crc32(b'Hello')  # Returns CRC32 of 'Hello'
    """
    ...
