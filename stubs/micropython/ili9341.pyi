"""Type stubs for ili9341 module (ILI9341 LCD display driver)."""

from typing import Any, Optional, Tuple
from machine import SPI, Pin

# Rotation constants
ROTATE_0: int
ROTATE_90: int
ROTATE_180: int
ROTATE_270: int

# Color constants (RGB565)
BLACK: int
WHITE: int
RED: int
GREEN: int
BLUE: int
CYAN: int
MAGENTA: int
YELLOW: int


class ILI9341:
    """ILI9341 320x240 LCD display driver.

    Example:
        from machine import Pin, SPI
        import ili9341

        spi = SPI(1, baudrate=40000000)
        display = ili9341.ILI9341(
            spi,
            cs=Pin(15),
            dc=Pin(2),
            rst=Pin(4)
        )

        display.fill(ili9341.BLACK)
        display.text("Hello!", 10, 10, ili9341.WHITE)
    """

    width: int
    height: int

    def __init__(
        self,
        spi: SPI,
        cs: Pin,
        dc: Pin,
        rst: Optional[Pin] = None,
        width: int = 320,
        height: int = 240,
        rotation: int = 0
    ) -> None:
        """Create ILI9341 display.

        Args:
            spi: SPI bus object
            cs: Chip select pin
            dc: Data/Command pin
            rst: Reset pin (optional)
            width: Display width
            height: Display height
            rotation: Initial rotation (0, 90, 180, 270)
        """
        ...

    def init(self) -> None:
        """Initialize display."""
        ...

    def reset(self) -> None:
        """Hardware reset display."""
        ...

    def set_rotation(self, rotation: int) -> None:
        """Set display rotation.

        Args:
            rotation: 0, 90, 180, or 270 degrees
        """
        ...

    def fill(self, color: int) -> None:
        """Fill display with color.

        Args:
            color: RGB565 color
        """
        ...

    def fill_rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Fill rectangle with color."""
        ...

    def pixel(self, x: int, y: int, color: int) -> None:
        """Set pixel color."""
        ...

    def hline(self, x: int, y: int, w: int, color: int) -> None:
        """Draw horizontal line."""
        ...

    def vline(self, x: int, y: int, h: int, color: int) -> None:
        """Draw vertical line."""
        ...

    def line(self, x0: int, y0: int, x1: int, y1: int, color: int) -> None:
        """Draw line."""
        ...

    def rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Draw rectangle outline."""
        ...

    def ellipse(self, x: int, y: int, rx: int, ry: int, color: int) -> None:
        """Draw ellipse outline."""
        ...

    def fill_ellipse(self, x: int, y: int, rx: int, ry: int, color: int) -> None:
        """Draw filled ellipse."""
        ...

    def circle(self, x: int, y: int, r: int, color: int) -> None:
        """Draw circle outline."""
        ...

    def fill_circle(self, x: int, y: int, r: int, color: int) -> None:
        """Draw filled circle."""
        ...

    def text(
        self,
        text: str,
        x: int,
        y: int,
        color: int = WHITE,
        background: int = BLACK,
        font: Any = None,
        scale: int = 1
    ) -> None:
        """Draw text.

        Args:
            text: String to display
            x: X position
            y: Y position
            color: Text color
            background: Background color
            font: Font module (optional)
            scale: Font scale multiplier
        """
        ...

    def image(self, path: str, x: int = 0, y: int = 0) -> None:
        """Display image from file.

        Args:
            path: Path to image file
            x: X position
            y: Y position
        """
        ...

    def blit(self, buf: bytes, x: int, y: int, w: int, h: int) -> None:
        """Blit buffer to display.

        Args:
            buf: RGB565 pixel data
            x: X position
            y: Y position
            w: Buffer width
            h: Buffer height
        """
        ...

    def scroll(self, dy: int) -> None:
        """Vertical scroll.

        Args:
            dy: Scroll amount in pixels
        """
        ...

    def sleep(self) -> None:
        """Enter sleep mode."""
        ...

    def wake(self) -> None:
        """Exit sleep mode."""
        ...

    def backlight_on(self) -> None:
        """Turn on backlight."""
        ...

    def backlight_off(self) -> None:
        """Turn off backlight."""
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
