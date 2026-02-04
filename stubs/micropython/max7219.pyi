"""Type stubs for max7219 module (MAX7219 LED matrix/7-segment driver)."""

from typing import Optional
from machine import SPI, Pin


class Matrix8x8:
    """MAX7219 8x8 LED matrix driver.

    Example:
        from machine import Pin, SPI
        from max7219 import Matrix8x8

        spi = SPI(1, baudrate=10000000)
        display = Matrix8x8(spi, Pin(15), 4)  # 4 cascaded matrices

        display.fill(0)
        display.text("Hi", 0, 0, 1)
        display.show()
    """

    def __init__(self, spi: SPI, cs: Pin, num: int = 1) -> None:
        """Create LED matrix driver.

        Args:
            spi: SPI bus object
            cs: Chip select pin
            num: Number of cascaded matrices
        """
        ...

    def brightness(self, value: int) -> None:
        """Set display brightness.

        Args:
            value: Brightness level (0-15)
        """
        ...

    def fill(self, color: int) -> None:
        """Fill display.

        Args:
            color: 0=off, 1=on
        """
        ...

    def pixel(self, x: int, y: int, color: Optional[int] = None) -> Optional[int]:
        """Get or set pixel.

        Args:
            x: X coordinate
            y: Y coordinate
            color: 0=off, 1=on, None=read

        Returns:
            Pixel state if reading
        """
        ...

    def hline(self, x: int, y: int, w: int, color: int) -> None:
        """Draw horizontal line."""
        ...

    def vline(self, x: int, y: int, h: int, color: int) -> None:
        """Draw vertical line."""
        ...

    def line(self, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
        """Draw line."""
        ...

    def rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Draw rectangle."""
        ...

    def fill_rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Draw filled rectangle."""
        ...

    def text(self, text: str, x: int, y: int, color: int = 1) -> None:
        """Draw text.

        Args:
            text: String to display
            x: X position
            y: Y position
            color: 0=off, 1=on
        """
        ...

    def scroll(self, dx: int, dy: int) -> None:
        """Scroll display contents.

        Args:
            dx: Horizontal scroll amount
            dy: Vertical scroll amount
        """
        ...

    def show(self) -> None:
        """Update display with buffer contents."""
        ...


class SevenSegment:
    """MAX7219 7-segment display driver.

    Example:
        from machine import Pin, SPI
        from max7219 import SevenSegment

        spi = SPI(1, baudrate=10000000)
        display = SevenSegment(spi, Pin(15), 8)  # 8 digits

        display.clear()
        display.write_number(1234)
        display.show()
    """

    def __init__(self, spi: SPI, cs: Pin, digits: int = 8) -> None:
        """Create 7-segment driver.

        Args:
            spi: SPI bus object
            cs: Chip select pin
            digits: Number of digits
        """
        ...

    def brightness(self, value: int) -> None:
        """Set brightness (0-15)."""
        ...

    def clear(self) -> None:
        """Clear display."""
        ...

    def write_number(
        self,
        number: float,
        decimals: int = 0,
        justify_right: bool = True
    ) -> None:
        """Display a number.

        Args:
            number: Number to display
            decimals: Decimal places
            justify_right: Right-justify the number
        """
        ...

    def write_text(self, text: str) -> None:
        """Display text (limited character set).

        Args:
            text: String to display (0-9, A-F, -, _, space, .)
        """
        ...

    def set_digit(self, digit: int, value: int, dp: bool = False) -> None:
        """Set individual digit.

        Args:
            digit: Digit position (0 = rightmost)
            value: Digit value (0-15)
            dp: Show decimal point
        """
        ...

    def show(self) -> None:
        """Update display."""
        ...
