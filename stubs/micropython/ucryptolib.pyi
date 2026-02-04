"""Type stubs for MicroPython ucryptolib module (cryptographic primitives)."""

from typing import Optional

# Mode constants
MODE_ECB: int  # Electronic Code Book
MODE_CBC: int  # Cipher Block Chaining
MODE_CTR: int  # Counter mode


class aes:
    """AES encryption/decryption.

    Example:
        from ucryptolib import aes

        # ECB mode (no IV needed)
        key = b'16bytekey1234567'
        cipher = aes(key, 1)  # MODE_ECB
        encrypted = cipher.encrypt(b'16 bytes of text')

        # CBC mode (requires 16-byte IV)
        iv = b'16byteiv12345678'
        cipher = aes(key, 2, iv)  # MODE_CBC
        encrypted = cipher.encrypt(b'16 bytes of text')
    """

    def __init__(
        self,
        key: bytes,
        mode: int,
        iv: Optional[bytes] = None
    ) -> None:
        """Create AES cipher.

        Args:
            key: Encryption key (16, 24, or 32 bytes for AES-128/192/256)
            mode: Cipher mode (MODE_ECB=1, MODE_CBC=2, MODE_CTR=6)
            iv: Initialization vector (16 bytes, required for CBC/CTR)
        """
        ...

    def encrypt(self, data: bytes, out: Optional[bytearray] = None) -> bytes:
        """Encrypt data.

        Args:
            data: Plaintext (must be multiple of 16 bytes for ECB/CBC)
            out: Optional output buffer

        Returns:
            Ciphertext bytes
        """
        ...

    def decrypt(self, data: bytes, out: Optional[bytearray] = None) -> bytes:
        """Decrypt data.

        Args:
            data: Ciphertext (must be multiple of 16 bytes for ECB/CBC)
            out: Optional output buffer

        Returns:
            Plaintext bytes
        """
        ...
