"""Type stubs for ssd1306 module (OLED display driver)."""

from typing import Optional
from machine import I2C, SPI, Pin
from framebuf import FrameBuffer


class SSD1306:
    """Base class for SSD1306 OLED displays.

    128x64 or 128x32 pixel monochrome OLED display.
    """

    width: int
    height: int
    buffer: bytearray

    def __init__(self, width: int, height: int, external_vcc: bool = False) -> None:
        """Initialize display.

        Args:
            width: Display width in pixels (usually 128)
            height: Display height in pixels (32 or 64)
            external_vcc: True if display has external power supply
        """
        ...

    def init_display(self) -> None:
        """Initialize display hardware."""
        ...

    def poweroff(self) -> None:
        """Turn off display."""
        ...

    def poweron(self) -> None:
        """Turn on display."""
        ...

    def contrast(self, contrast: int) -> None:
        """Set display contrast.

        Args:
            contrast: Contrast value (0-255)
        """
        ...

    def invert(self, invert: bool) -> None:
        """Invert display colors.

        Args:
            invert: True to invert, False for normal
        """
        ...

    def rotate(self, rotate: bool) -> None:
        """Rotate display 180 degrees.

        Args:
            rotate: True to rotate, False for normal
        """
        ...

    def show(self) -> None:
        """Update display with buffer contents.

        Call this after drawing to see changes.
        """
        ...

    # FrameBuffer methods (inherited)
    def fill(self, color: int) -> None:
        """Fill display with color (0=black, 1=white)."""
        ...

    def pixel(self, x: int, y: int, color: Optional[int] = None) -> Optional[int]:
        """Get or set pixel."""
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
        """Draw rectangle outline."""
        ...

    def fill_rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Draw filled rectangle."""
        ...

    def text(self, text: str, x: int, y: int, color: int = 1) -> None:
        """Draw text using 8x8 font."""
        ...

    def scroll(self, xstep: int, ystep: int) -> None:
        """Scroll display contents."""
        ...

    def blit(self, fbuf: FrameBuffer, x: int, y: int, key: int = -1) -> None:
        """Copy framebuffer to display."""
        ...


class SSD1306_I2C(SSD1306):
    """SSD1306 OLED display over I2C.

    Example:
        from machine import Pin, I2C
        from ssd1306 import SSD1306_I2C

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        oled = SSD1306_I2C(128, 64, i2c)

        oled.fill(0)
        oled.text("Hello!", 0, 0, 1)
        oled.show()
    """

    def __init__(
        self,
        width: int,
        height: int,
        i2c: I2C,
        addr: int = 0x3C,
        external_vcc: bool = False
    ) -> None:
        """Create I2C display.

        Args:
            width: Display width (128)
            height: Display height (32 or 64)
            i2c: I2C bus object
            addr: I2C address (usually 0x3C or 0x3D)
            external_vcc: External power supply
        """
        ...


class SSD1306_SPI(SSD1306):
    """SSD1306 OLED display over SPI.

    Example:
        from machine import Pin, SPI
        from ssd1306 import SSD1306_SPI

        spi = SPI(1, baudrate=10000000)
        oled = SSD1306_SPI(128, 64, spi, Pin(4), Pin(5), Pin(2))

        oled.fill(0)
        oled.text("Hello!", 0, 0, 1)
        oled.show()
    """

    def __init__(
        self,
        width: int,
        height: int,
        spi: SPI,
        dc: Pin,
        res: Pin,
        cs: Pin,
        external_vcc: bool = False
    ) -> None:
        """Create SPI display.

        Args:
            width: Display width (128)
            height: Display height (32 or 64)
            spi: SPI bus object
            dc: Data/Command pin
            res: Reset pin
            cs: Chip select pin
            external_vcc: External power supply
        """
        ...
