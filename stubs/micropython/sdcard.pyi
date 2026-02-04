"""Type stubs for sdcard module (SD card via SPI)."""

from typing import Tuple
from machine import SPI, Pin


class SDCard:
    """SD card interface via SPI.

    Example:
        from machine import Pin, SPI
        import sdcard
        import uos

        spi = SPI(1, baudrate=1000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
        sd = sdcard.SDCard(spi, Pin(15))

        # Mount the filesystem
        uos.mount(sd, '/sd')

        # Now you can use /sd as a normal filesystem
        with open('/sd/test.txt', 'w') as f:
            f.write('Hello SD card!')

        # List files
        print(uos.listdir('/sd'))

        # Unmount when done
        uos.umount('/sd')
    """

    def __init__(
        self,
        spi: SPI,
        cs: Pin,
        baudrate: int = 1320000
    ) -> None:
        """Create SD card interface.

        Args:
            spi: SPI bus object
            cs: Chip select pin
            baudrate: SPI baudrate for data transfer
        """
        ...

    def init_card(self) -> None:
        """Initialize the SD card."""
        ...

    def readblocks(self, block_num: int, buf: bytearray) -> None:
        """Read blocks from SD card.

        Args:
            block_num: Starting block number
            buf: Buffer to read into
        """
        ...

    def writeblocks(self, block_num: int, buf: bytes) -> None:
        """Write blocks to SD card.

        Args:
            block_num: Starting block number
            buf: Data to write
        """
        ...

    def ioctl(self, op: int, arg: int = 0) -> int:
        """Control SD card.

        Args:
            op: Operation code
            arg: Operation argument

        Operations:
            1: Initialize (arg ignored)
            4: Get block count
            5: Get block size (512)
        """
        ...


class SDCardError(Exception):
    """SD card error."""
    pass
