"""Type stubs for sh1106 module (SH1106 OLED display driver)."""

from typing import Optional
from machine import I2C, SPI, Pin
from framebuf import FrameBuffer


class SH1106:
    """Base class for SH1106 OLED displays.

    Similar to SSD1306 but with slightly different controller.
    Common sizes: 128x64, 128x32.
    """

    width: int
    height: int

    def __init__(self, width: int, height: int, external_vcc: bool = False) -> None:
        """Initialize display."""
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
        """Set contrast (0-255)."""
        ...

    def invert(self, invert: bool) -> None:
        """Invert display colors."""
        ...

    def rotate(self, rotate: bool) -> None:
        """Rotate display 180 degrees."""
        ...

    def show(self) -> None:
        """Update display with buffer contents."""
        ...

    def fill(self, color: int) -> None:
        """Fill display with color."""
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
        """Draw rectangle."""
        ...

    def fill_rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Draw filled rectangle."""
        ...

    def text(self, text: str, x: int, y: int, color: int = 1) -> None:
        """Draw text."""
        ...

    def scroll(self, xstep: int, ystep: int) -> None:
        """Scroll display."""
        ...


class SH1106_I2C(SH1106):
    """SH1106 OLED display over I2C.

    Example:
        from machine import Pin, I2C
        from sh1106 import SH1106_I2C

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        oled = SH1106_I2C(128, 64, i2c)

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
            addr: I2C address (0x3C or 0x3D)
            external_vcc: External power supply
        """
        ...


class SH1106_SPI(SH1106):
    """SH1106 OLED display over SPI.

    Example:
        from machine import Pin, SPI
        from sh1106 import SH1106_SPI

        spi = SPI(1, baudrate=10000000)
        oled = SH1106_SPI(128, 64, spi, Pin(4), Pin(5), Pin(2))

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
            width: Display width
            height: Display height
            spi: SPI bus object
            dc: Data/Command pin
            res: Reset pin
            cs: Chip select pin
            external_vcc: External power supply
        """
        ...
