"""Type stubs for MicroPython uhashlib module (hashing algorithms)."""

from typing import Union


class sha256:
    """SHA256 hash algorithm.

    Example:
        h = uhashlib.sha256()
        h.update(b'Hello')
        h.update(b' World')
        print(h.digest())  # 32-byte hash
    """

    def __init__(self, data: bytes = b"") -> None:
        """Create SHA256 hash object.

        Args:
            data: Initial data to hash
        """
        ...

    def update(self, data: bytes) -> None:
        """Add data to hash.

        Args:
            data: Data to hash
        """
        ...

    def digest(self) -> bytes:
        """Return hash value as bytes.

        Returns:
            32-byte SHA256 digest
        """
        ...

    def hexdigest(self) -> str:
        """Return hash value as hex string.

        Returns:
            64-character hex string
        """
        ...

    def copy(self) -> "sha256":
        """Return copy of hash object."""
        ...


class sha1:
    """SHA1 hash algorithm (160-bit).

    Note: SHA1 is considered weak for cryptographic purposes.
    """

    def __init__(self, data: bytes = b"") -> None:
        """Create SHA1 hash object."""
        ...

    def update(self, data: bytes) -> None:
        """Add data to hash."""
        ...

    def digest(self) -> bytes:
        """Return 20-byte hash value."""
        ...

    def hexdigest(self) -> str:
        """Return 40-character hex string."""
        ...

    def copy(self) -> "sha1":
        """Return copy of hash object."""
        ...


class md5:
    """MD5 hash algorithm (128-bit).

    Note: MD5 is considered broken for cryptographic purposes.
    Only use for checksums, not security.
    """

    def __init__(self, data: bytes = b"") -> None:
        """Create MD5 hash object."""
        ...

    def update(self, data: bytes) -> None:
        """Add data to hash."""
        ...

    def digest(self) -> bytes:
        """Return 16-byte hash value."""
        ...

    def hexdigest(self) -> str:
        """Return 32-character hex string."""
        ...

    def copy(self) -> "md5":
        """Return copy of hash object."""
        ...


class sha512:
    """SHA512 hash algorithm (512-bit).

    Note: Not available on all MicroPython ports.
    """

    def __init__(self, data: bytes = b"") -> None:
        """Create SHA512 hash object."""
        ...

    def update(self, data: bytes) -> None:
        """Add data to hash."""
        ...

    def digest(self) -> bytes:
        """Return 64-byte hash value."""
        ...

    def hexdigest(self) -> str:
        """Return 128-character hex string."""
        ...

    def copy(self) -> "sha512":
        """Return copy of hash object."""
        ...
