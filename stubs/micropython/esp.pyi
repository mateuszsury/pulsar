"""Type stubs for MicroPython esp module (common ESP functions)."""

from typing import Optional

# Flash size constants
FLASH_SIZE: int

def sleep_type(sleep_type: Optional[int] = None) -> Optional[int]:
    """Get/set sleep type for modem sleep."""
    ...

def deepsleep(time_us: int = 0) -> None:
    """Enter deep sleep mode.

    Args:
        time_us: Sleep duration in microseconds (0 = indefinite)
    """
    ...

def flash_id() -> int:
    """Get the flash chip ID."""
    ...

def flash_size() -> int:
    """Get the flash chip size in bytes."""
    ...

def flash_user_start() -> int:
    """Get the start address of user flash area."""
    ...

def flash_read(byte_offset: int, length_or_buffer: int) -> bytes:
    """Read from flash memory.

    Args:
        byte_offset: Offset in flash
        length_or_buffer: Number of bytes or buffer

    Returns:
        Bytes read from flash
    """
    ...

def flash_write(byte_offset: int, buf: bytes) -> None:
    """Write to flash memory.

    Args:
        byte_offset: Offset in flash (must be 4-byte aligned)
        buf: Data to write (length must be multiple of 4)
    """
    ...

def flash_erase(sector_no: int) -> None:
    """Erase a flash sector (4KB).

    Args:
        sector_no: Sector number
    """
    ...

def osdebug(level: Optional[int]) -> None:
    """Set or disable ESP-IDF log output.

    Args:
        level: Log level (None to disable)
    """
    ...

def gpio_matrix_in(
    gpio: int,
    sig: int,
    inv: bool = False
) -> None:
    """Route a GPIO to a peripheral signal input.

    Args:
        gpio: GPIO number
        sig: Signal number
        inv: Invert signal
    """
    ...

def gpio_matrix_out(
    gpio: int,
    sig: int,
    out_inv: bool = False,
    out_en_inv: bool = False
) -> None:
    """Route a peripheral signal to a GPIO output.

    Args:
        gpio: GPIO number
        sig: Signal number
        out_inv: Invert output
        out_en_inv: Invert output enable
    """
    ...
