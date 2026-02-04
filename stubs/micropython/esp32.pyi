"""Type stubs for MicroPython esp32 module (ESP32-specific)."""

from typing import Any, Callable, Optional, Tuple

# Wake sources
WAKEUP_ALL_LOW: bool
WAKEUP_ANY_HIGH: bool

# ULP constants
ULP_WAKEUP_PERIOD: int

def wake_on_touch(wake: bool) -> None:
    """Enable/disable wake from touch pad."""
    ...

def wake_on_ext0(pin: Any, level: int) -> None:
    """Configure EXT0 wake source (single pin).

    Args:
        pin: Pin object
        level: 0 for low, 1 for high
    """
    ...

def wake_on_ext1(pins: tuple, level: int) -> None:
    """Configure EXT1 wake source (multiple pins).

    Args:
        pins: Tuple of pin objects
        level: WAKEUP_ALL_LOW or WAKEUP_ANY_HIGH
    """
    ...

def gpio_deep_sleep_hold(enable: bool) -> None:
    """Enable/disable GPIO pin hold during deep sleep."""
    ...

def raw_temperature() -> int:
    """Read the internal temperature sensor (raw value).

    Returns:
        Raw temperature value (need calibration for Celsius)
    """
    ...

def hall_sensor() -> int:
    """Read the internal hall effect sensor.

    Returns:
        Hall sensor reading
    """
    ...

def idf_heap_info(capabilities: int) -> list[Tuple[int, int, int, int, int]]:
    """Get ESP-IDF heap information.

    Args:
        capabilities: Capability flags

    Returns:
        List of tuples with heap info
    """
    ...


class Partition:
    """ESP32 partition access."""

    BOOT: int
    RUNNING: int
    TYPE_APP: int
    TYPE_DATA: int

    def __init__(
        self,
        id: Any,
        block_size: int = 4096,
        *,
        type: int = TYPE_APP,
        subtype: int = 0xff
    ) -> None:
        """Create partition object.

        Args:
            id: Partition name, BOOT, or RUNNING
            block_size: Block size for block device operations
            type: Partition type
            subtype: Partition subtype
        """
        ...

    @classmethod
    def find(
        cls,
        type: int = TYPE_APP,
        subtype: int = 0xff,
        label: Optional[str] = None,
        block_size: int = 4096
    ) -> list["Partition"]:
        """Find partitions matching criteria.

        Args:
            type: Partition type
            subtype: Partition subtype
            label: Partition label
            block_size: Block size

        Returns:
            List of matching Partition objects
        """
        ...

    def info(self) -> Tuple[int, int, int, int, str, bool]:
        """Get partition information.

        Returns:
            Tuple of (type, subtype, address, size, label, encrypted)
        """
        ...

    def readblocks(
        self,
        block_num: int,
        buf: bytearray,
        offset: int = 0
    ) -> None:
        """Read blocks from partition."""
        ...

    def writeblocks(
        self,
        block_num: int,
        buf: bytes,
        offset: int = 0
    ) -> None:
        """Write blocks to partition."""
        ...

    def ioctl(self, cmd: int, arg: Any = None) -> Any:
        """Partition I/O control."""
        ...

    def set_boot(self) -> None:
        """Set this partition as the boot partition."""
        ...

    def get_next_update(self) -> "Partition":
        """Get the next OTA update partition."""
        ...

    @staticmethod
    def mark_app_valid_cancel_rollback() -> None:
        """Mark the running app as valid (prevent rollback)."""
        ...


class RMT:
    """Remote Control (RMT) peripheral."""

    PULSE_MAX: int

    def __init__(
        self,
        channel: int,
        *,
        pin: Optional[Any] = None,
        clock_div: int = 8,
        idle_level: bool = False,
        tx_carrier: Optional[Tuple[int, int, bool]] = None
    ) -> None:
        """Create RMT channel.

        Args:
            channel: RMT channel number (0-7)
            pin: GPIO pin for TX/RX
            clock_div: Clock divider (1-255)
            idle_level: Idle output level
            tx_carrier: Carrier config (freq, duty, level)
        """
        ...

    def source_freq(self) -> int:
        """Get the source clock frequency."""
        ...

    def clock_div(self) -> int:
        """Get the clock divider."""
        ...

    def wait_done(self, *, timeout: int = 0) -> bool:
        """Wait for transmission to complete.

        Args:
            timeout: Timeout in milliseconds (0 = no timeout)

        Returns:
            True if done, False if timeout
        """
        ...

    def loop(self, enable: bool) -> None:
        """Enable/disable continuous transmission loop."""
        ...

    def write_pulses(
        self,
        pulses: tuple,
        start: int = 1
    ) -> None:
        """Send pulse sequence.

        Args:
            pulses: Tuple of pulse durations in clock ticks
            start: Initial output level
        """
        ...

    def bitstream_channel(
        self,
        value: Optional[int] = None
    ) -> int:
        """Get/set the bitstream channel."""
        ...

    @staticmethod
    def bitstream_channel(value: Optional[int] = None) -> int:
        """Get/set the global bitstream channel."""
        ...


class ULP:
    """Ultra Low Power coprocessor."""

    RESERVE_MEM: int

    def __init__(self) -> None:
        """Create ULP instance."""
        ...

    def set_wakeup_period(self, period_index: int, period_us: int) -> None:
        """Set ULP wakeup period.

        Args:
            period_index: Period index (0-4)
            period_us: Period in microseconds
        """
        ...

    def load_binary(self, load_addr: int, program_binary: bytes) -> None:
        """Load ULP binary program.

        Args:
            load_addr: Load address in ULP memory
            program_binary: Binary program data
        """
        ...

    def run(self, entry_point: int) -> None:
        """Run ULP program from entry point."""
        ...


class NVS:
    """Non-Volatile Storage namespace."""

    def __init__(self, namespace: str) -> None:
        """Open NVS namespace.

        Args:
            namespace: Namespace name (max 15 chars)
        """
        ...

    def set_i32(self, key: str, value: int) -> None:
        """Store 32-bit signed integer."""
        ...

    def get_i32(self, key: str) -> int:
        """Get 32-bit signed integer."""
        ...

    def set_blob(self, key: str, value: bytes) -> None:
        """Store binary blob."""
        ...

    def get_blob(self, key: str, buffer: bytearray) -> int:
        """Get binary blob into buffer.

        Returns:
            Length of data read
        """
        ...

    def erase_key(self, key: str) -> None:
        """Erase a key from NVS."""
        ...

    def commit(self) -> None:
        """Commit changes to flash."""
        ...
