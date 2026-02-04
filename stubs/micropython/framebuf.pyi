"""Type stubs for MicroPython framebuf module (frame buffer for displays)."""

from typing import Optional

# Format constants
MONO_VLSB: int  # Monochrome, vertical LSB
MONO_HLSB: int  # Monochrome, horizontal LSB
MONO_HMSB: int  # Monochrome, horizontal MSB
RGB565: int     # 16-bit color (5-6-5)
GS2_HMSB: int   # 2-bit grayscale
GS4_HMSB: int   # 4-bit grayscale
GS8: int        # 8-bit grayscale


class FrameBuffer:
    """Frame buffer for graphics operations.

    Used for drawing graphics and text on displays.

    Example:
        import framebuf

        # Create 128x64 monochrome buffer
        buf = bytearray(128 * 64 // 8)
        fb = framebuf.FrameBuffer(buf, 128, 64, framebuf.MONO_HLSB)

        fb.fill(0)  # Clear
        fb.text("Hello", 0, 0, 1)
        fb.rect(10, 10, 50, 30, 1)
    """

    def __init__(
        self,
        buffer: bytearray,
        width: int,
        height: int,
        format: int,
        stride: Optional[int] = None
    ) -> None:
        """Create frame buffer.

        Args:
            buffer: Underlying data buffer
            width: Width in pixels
            height: Height in pixels
            format: Pixel format (MONO_VLSB, RGB565, etc.)
            stride: Number of pixels between rows (default = width)
        """
        ...

    def fill(self, color: int) -> None:
        """Fill entire buffer with color.

        Args:
            color: Fill color (0 or 1 for mono, 0-65535 for RGB565)
        """
        ...

    def pixel(self, x: int, y: int, color: Optional[int] = None) -> Optional[int]:
        """Get or set pixel.

        Args:
            x: X coordinate
            y: Y coordinate
            color: Color to set, or None to read

        Returns:
            Pixel color if reading, None if writing
        """
        ...

    def hline(self, x: int, y: int, w: int, color: int) -> None:
        """Draw horizontal line.

        Args:
            x: Start X coordinate
            y: Y coordinate
            w: Width in pixels
            color: Line color
        """
        ...

    def vline(self, x: int, y: int, h: int, color: int) -> None:
        """Draw vertical line.

        Args:
            x: X coordinate
            y: Start Y coordinate
            h: Height in pixels
            color: Line color
        """
        ...

    def line(self, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
        """Draw line between two points.

        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates
            color: Line color
        """
        ...

    def rect(self, x: int, y: int, w: int, h: int, color: int, fill: bool = False) -> None:
        """Draw rectangle.

        Args:
            x, y: Top-left corner
            w: Width
            h: Height
            color: Border/fill color
            fill: Fill the rectangle if True
        """
        ...

    def fill_rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Draw filled rectangle.

        Args:
            x, y: Top-left corner
            w: Width
            h: Height
            color: Fill color
        """
        ...

    def ellipse(
        self,
        x: int,
        y: int,
        xr: int,
        yr: int,
        color: int,
        fill: bool = False,
        m: int = 0xf
    ) -> None:
        """Draw ellipse.

        Args:
            x, y: Center coordinates
            xr: X radius
            yr: Y radius
            color: Color
            fill: Fill the ellipse
            m: Quadrant mask (1=Q1, 2=Q2, 4=Q3, 8=Q4)
        """
        ...

    def poly(
        self,
        x: int,
        y: int,
        coords: list,
        color: int,
        fill: bool = False
    ) -> None:
        """Draw polygon.

        Args:
            x, y: Origin offset
            coords: List of (x, y) coordinate pairs
            color: Color
            fill: Fill the polygon
        """
        ...

    def text(self, s: str, x: int, y: int, color: int = 1) -> None:
        """Draw text using built-in 8x8 font.

        Args:
            s: String to draw
            x: X coordinate
            y: Y coordinate
            color: Text color
        """
        ...

    def scroll(self, xstep: int, ystep: int) -> None:
        """Scroll buffer contents.

        Args:
            xstep: Horizontal scroll amount
            ystep: Vertical scroll amount
        """
        ...

    def blit(
        self,
        fbuf: "FrameBuffer",
        x: int,
        y: int,
        key: int = -1,
        palette: Optional["FrameBuffer"] = None
    ) -> None:
        """Copy another FrameBuffer to this one.

        Args:
            fbuf: Source FrameBuffer
            x, y: Destination coordinates
            key: Transparent color (-1 = none)
            palette: Color lookup palette
        """
        ...


def rgb565(r: int, g: int, b: int) -> int:
    """Convert RGB to RGB565 format.

    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)

    Returns:
        16-bit RGB565 color value
    """
    ...
