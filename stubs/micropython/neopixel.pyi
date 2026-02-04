"""Type stubs for MicroPython neopixel module (WS2812/NeoPixel LEDs)."""

from typing import Tuple, Union
from machine import Pin


class NeoPixel:
    """Control WS2812 (NeoPixel) addressable RGB/RGBW LEDs.

    Example:
        from machine import Pin
        from neopixel import NeoPixel

        np = NeoPixel(Pin(5), 8)  # 8 LEDs on GPIO5
        np[0] = (255, 0, 0)  # Set first LED to red
        np.write()  # Update LEDs
    """

    ORDER: Tuple[int, int, int]  # Default RGB order

    def __init__(
        self,
        pin: Pin,
        n: int,
        *,
        bpp: int = 3,
        timing: int = 1
    ) -> None:
        """Create NeoPixel controller.

        Args:
            pin: Output pin connected to LED data input
            n: Number of LEDs in the strip
            bpp: Bytes per pixel (3 for RGB, 4 for RGBW)
            timing: Timing mode (0 for 400kHz, 1 for 800kHz WS2812)
        """
        ...

    @property
    def n(self) -> int:
        """Number of LEDs."""
        ...

    @property
    def bpp(self) -> int:
        """Bytes per pixel (3=RGB, 4=RGBW)."""
        ...

    def __len__(self) -> int:
        """Return number of LEDs."""
        ...

    def __getitem__(
        self,
        index: int
    ) -> Union[Tuple[int, int, int], Tuple[int, int, int, int]]:
        """Get LED color.

        Args:
            index: LED index (0 to n-1)

        Returns:
            Tuple of (R, G, B) or (R, G, B, W)
        """
        ...

    def __setitem__(
        self,
        index: int,
        value: Union[Tuple[int, int, int], Tuple[int, int, int, int]]
    ) -> None:
        """Set LED color.

        Args:
            index: LED index (0 to n-1)
            value: Color tuple (R, G, B) or (R, G, B, W), values 0-255
        """
        ...

    def fill(
        self,
        color: Union[Tuple[int, int, int], Tuple[int, int, int, int]]
    ) -> None:
        """Fill all LEDs with a color.

        Args:
            color: Color tuple (R, G, B) or (R, G, B, W)
        """
        ...

    def write(self) -> None:
        """Write colors to the LED strip.

        Call this after setting colors to update the physical LEDs.
        """
        ...

    def buf(self) -> bytearray:
        """Return the underlying buffer."""
        ...
