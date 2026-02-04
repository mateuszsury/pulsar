"""Type stubs for st7789 module (ST7789 LCD display driver)."""

from typing import Optional, Tuple
from machine import SPI, Pin

# Color constants
BLACK: int
BLUE: int
RED: int
GREEN: int
CYAN: int
MAGENTA: int
YELLOW: int
WHITE: int

# Rotation constants
PORTRAIT: int
LANDSCAPE: int
INVERTED_PORTRAIT: int
INVERTED_LANDSCAPE: int


class ST7789:
    """ST7789 LCD display driver.

    Supports 240x240, 240x320, and other ST7789 displays.

    Example:
        from machine import Pin, SPI
        import st7789

        spi = SPI(1, baudrate=40000000, polarity=1)
        display = st7789.ST7789(
            spi, 240, 240,
            reset=Pin(4, Pin.OUT),
            dc=Pin(2, Pin.OUT)
        )

        display.fill(st7789.BLACK)
        display.text("Hello!", 10, 10, st7789.WHITE)
    """

    def __init__(
        self,
        spi: SPI,
        width: int,
        height: int,
        reset: Optional[Pin] = None,
        dc: Optional[Pin] = None,
        cs: Optional[Pin] = None,
        backlight: Optional[Pin] = None,
        rotation: int = 0,
        color_order: int = 0,
        inversion: bool = True,
        options: int = 0
    ) -> None:
        """Create ST7789 display.

        Args:
            spi: SPI bus object
            width: Display width in pixels
            height: Display height in pixels
            reset: Reset pin (optional)
            dc: Data/Command pin
            cs: Chip select pin (optional)
            backlight: Backlight control pin (optional)
            rotation: Display rotation (0, 90, 180, 270)
            color_order: RGB or BGR color order
            inversion: Enable color inversion
            options: Additional options
        """
        ...

    def init(self) -> None:
        """Initialize display."""
        ...

    def on(self) -> None:
        """Turn on display."""
        ...

    def off(self) -> None:
        """Turn off display."""
        ...

    def sleep_mode(self, value: bool) -> None:
        """Enter or exit sleep mode."""
        ...

    def inversion_mode(self, value: bool) -> None:
        """Set color inversion mode."""
        ...

    def rotation(self, rotation: int) -> None:
        """Set display rotation.

        Args:
            rotation: 0, 90, 180, or 270 degrees
        """
        ...

    def fill(self, color: int) -> None:
        """Fill display with color.

        Args:
            color: RGB565 color value
        """
        ...

    def fill_rect(self, x: int, y: int, width: int, height: int, color: int) -> None:
        """Fill rectangle with color."""
        ...

    def pixel(self, x: int, y: int, color: int) -> None:
        """Set pixel color."""
        ...

    def hline(self, x: int, y: int, length: int, color: int) -> None:
        """Draw horizontal line."""
        ...

    def vline(self, x: int, y: int, length: int, color: int) -> None:
        """Draw vertical line."""
        ...

    def line(self, x0: int, y0: int, x1: int, y1: int, color: int) -> None:
        """Draw line between two points."""
        ...

    def rect(self, x: int, y: int, width: int, height: int, color: int) -> None:
        """Draw rectangle outline."""
        ...

    def text(
        self,
        font: Any,
        text: str,
        x: int,
        y: int,
        color: int = WHITE,
        background: int = BLACK
    ) -> int:
        """Draw text using font.

        Args:
            font: Font module
            text: String to draw
            x: X position
            y: Y position
            color: Text color
            background: Background color

        Returns:
            Width of drawn text
        """
        ...

    def bitmap(self, bitmap: Any, x: int, y: int, index: int = 0) -> None:
        """Draw bitmap image.

        Args:
            bitmap: Bitmap module
            x: X position
            y: Y position
            index: Bitmap index (for sprite sheets)
        """
        ...

    def blit_buffer(
        self,
        buffer: bytes,
        x: int,
        y: int,
        width: int,
        height: int
    ) -> None:
        """Copy buffer to display.

        Args:
            buffer: RGB565 pixel data
            x: X position
            y: Y position
            width: Buffer width
            height: Buffer height
        """
        ...

    def scroll(self, xstep: int = 0, ystep: int = 0) -> None:
        """Scroll display contents."""
        ...

    @staticmethod
    def color565(r: int, g: int, b: int) -> int:
        """Convert RGB to RGB565.

        Args:
            r: Red (0-255)
            g: Green (0-255)
            b: Blue (0-255)

        Returns:
            RGB565 color value
        """
        ...

    def width(self) -> int:
        """Get display width."""
        ...

    def height(self) -> int:
        """Get display height."""
        ...
