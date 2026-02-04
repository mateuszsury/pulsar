"""Type stubs for MicroPython machine module."""

from typing import Any, Callable, Optional, Tuple, Union, overload

# Memory access objects
mem8: Any
mem16: Any
mem32: Any

# Reset causes
PWRON_RESET: int
HARD_RESET: int
WDT_RESET: int
DEEPSLEEP_RESET: int
SOFT_RESET: int

# Wake reasons
PIN_WAKE: int
EXT0_WAKE: int
EXT1_WAKE: int
TIMER_WAKE: int
TOUCHPAD_WAKE: int
ULP_WAKE: int

def reset() -> None:
    """Reset the device."""
    ...

def soft_reset() -> None:
    """Perform a soft reset."""
    ...

def reset_cause() -> int:
    """Return the reset cause."""
    ...

def wake_reason() -> int:
    """Return the wake reason from sleep."""
    ...

@overload
def freq() -> int:
    """Get CPU frequency in Hz."""
    ...

@overload
def freq(hz: int) -> None:
    """Set CPU frequency in Hz."""
    ...

def unique_id() -> bytes:
    """Return the unique identifier of the chip."""
    ...

def idle() -> None:
    """Enter idle mode, reducing power consumption."""
    ...

def sleep() -> None:
    """Enter sleep mode (alias for lightsleep)."""
    ...

def lightsleep(time_ms: Optional[int] = None) -> None:
    """Enter light sleep mode.

    Args:
        time_ms: Sleep duration in milliseconds. If None, sleep indefinitely.
    """
    ...

def deepsleep(time_ms: Optional[int] = None) -> None:
    """Enter deep sleep mode.

    Args:
        time_ms: Sleep duration in milliseconds. If None, sleep indefinitely.
    """
    ...

def disable_irq() -> int:
    """Disable interrupt requests. Returns previous IRQ state."""
    ...

def enable_irq(state: int) -> None:
    """Re-enable interrupt requests."""
    ...

def time_pulse_us(
    pin: "Pin",
    pulse_level: int,
    timeout_us: int = 1000000
) -> int:
    """Time a pulse on a pin in microseconds."""
    ...

def bitstream(
    pin: "Pin",
    encoding: int,
    timing: Tuple[int, ...],
    data: bytes
) -> None:
    """Transmit data using precise bit timing."""
    ...


class Pin:
    """GPIO pin control class."""

    # Pin modes
    IN: int
    OUT: int
    OPEN_DRAIN: int
    ALT: int
    ALT_OPEN_DRAIN: int

    # Pull resistor modes
    PULL_UP: int
    PULL_DOWN: int
    PULL_HOLD: int

    # IRQ triggers
    IRQ_RISING: int
    IRQ_FALLING: int
    IRQ_LOW_LEVEL: int
    IRQ_HIGH_LEVEL: int

    # Drive strength
    DRIVE_0: int
    DRIVE_1: int
    DRIVE_2: int
    DRIVE_3: int

    def __init__(
        self,
        id: Union[int, str],
        mode: int = -1,
        pull: int = -1,
        *,
        value: Optional[int] = None,
        drive: Optional[int] = None,
        alt: Optional[int] = None
    ) -> None:
        """Initialize a GPIO pin.

        Args:
            id: Pin number or name
            mode: IN, OUT, OPEN_DRAIN, ALT, or ALT_OPEN_DRAIN
            pull: PULL_UP, PULL_DOWN, or PULL_HOLD
            value: Initial output value
            drive: Drive strength (DRIVE_0 to DRIVE_3)
            alt: Alternate function number
        """
        ...

    def init(
        self,
        mode: int = -1,
        pull: int = -1,
        *,
        value: Optional[int] = None,
        drive: Optional[int] = None,
        alt: Optional[int] = None
    ) -> None:
        """Re-initialize the pin."""
        ...

    @overload
    def value(self) -> int:
        """Get the pin value (0 or 1)."""
        ...

    @overload
    def value(self, x: int) -> None:
        """Set the pin value."""
        ...

    def __call__(self, x: Optional[int] = None) -> Optional[int]:
        """Shorthand for value()."""
        ...

    def on(self) -> None:
        """Set pin to high (1)."""
        ...

    def off(self) -> None:
        """Set pin to low (0)."""
        ...

    def irq(
        self,
        handler: Optional[Callable[["Pin"], None]] = None,
        trigger: int = IRQ_FALLING | IRQ_RISING,
        *,
        priority: int = 1,
        wake: Optional[int] = None,
        hard: bool = False
    ) -> Callable[..., Any]:
        """Configure an interrupt handler.

        Args:
            handler: Function to call on interrupt
            trigger: IRQ_RISING, IRQ_FALLING, or both
            priority: Interrupt priority
            wake: Wake mode for sleep
            hard: Use hard interrupt handler
        """
        ...


class Signal:
    """Control a pin with optional inversion."""

    def __init__(
        self,
        pin: Pin,
        invert: bool = False
    ) -> None:
        """Create a Signal from a Pin.

        Args:
            pin: The Pin object to control
            invert: Whether to invert the logic level
        """
        ...

    @overload
    def value(self) -> int:
        """Get signal value."""
        ...

    @overload
    def value(self, x: int) -> None:
        """Set signal value."""
        ...

    def on(self) -> None:
        """Set signal active."""
        ...

    def off(self) -> None:
        """Set signal inactive."""
        ...


class ADC:
    """Analog-to-Digital Converter."""

    # Attenuation levels (ESP32)
    ATTN_0DB: int
    ATTN_2_5DB: int
    ATTN_6DB: int
    ATTN_11DB: int

    # Resolution
    WIDTH_9BIT: int
    WIDTH_10BIT: int
    WIDTH_11BIT: int
    WIDTH_12BIT: int

    def __init__(self, pin: Union[Pin, int]) -> None:
        """Create ADC on a pin.

        Args:
            pin: Pin object or pin number
        """
        ...

    def read(self) -> int:
        """Read the ADC value."""
        ...

    def read_u16(self) -> int:
        """Read ADC value as 16-bit unsigned integer."""
        ...

    def read_uv(self) -> int:
        """Read ADC value in microvolts."""
        ...

    def atten(self, attenuation: int) -> None:
        """Set attenuation level."""
        ...

    def width(self, width: int) -> None:
        """Set ADC resolution width."""
        ...


class ADCBlock:
    """ADC block for accessing multiple channels."""

    def __init__(self, id: int, *, bits: int = 12) -> None:
        ...

    def init(self, *, bits: int = 12) -> None:
        ...

    def connect(
        self,
        channel: int,
        pin: Optional[Pin] = None
    ) -> ADC:
        """Connect a channel to an ADC."""
        ...


class DAC:
    """Digital-to-Analog Converter (ESP32 only)."""

    def __init__(self, pin: Union[Pin, int]) -> None:
        """Create DAC on pin 25 or 26 (ESP32).

        Args:
            pin: Pin 25 or 26
        """
        ...

    def write(self, value: int) -> None:
        """Write value (0-255) to DAC."""
        ...


class PWM:
    """Pulse Width Modulation output."""

    def __init__(
        self,
        pin: Pin,
        *,
        freq: int = 0,
        duty: int = 0,
        duty_u16: int = 0,
        duty_ns: int = 0
    ) -> None:
        """Create PWM output on a pin.

        Args:
            pin: Pin to output PWM on
            freq: PWM frequency in Hz
            duty: Duty cycle (0-1023)
            duty_u16: Duty cycle as 16-bit value
            duty_ns: Duty cycle in nanoseconds
        """
        ...

    def init(
        self,
        *,
        freq: Optional[int] = None,
        duty: Optional[int] = None,
        duty_u16: Optional[int] = None,
        duty_ns: Optional[int] = None
    ) -> None:
        """Reinitialize PWM with new parameters."""
        ...

    def deinit(self) -> None:
        """Disable PWM output."""
        ...

    @overload
    def freq(self) -> int:
        """Get PWM frequency."""
        ...

    @overload
    def freq(self, value: int) -> None:
        """Set PWM frequency."""
        ...

    @overload
    def duty(self) -> int:
        """Get duty cycle (0-1023)."""
        ...

    @overload
    def duty(self, value: int) -> None:
        """Set duty cycle (0-1023)."""
        ...

    @overload
    def duty_u16(self) -> int:
        """Get duty cycle as 16-bit value."""
        ...

    @overload
    def duty_u16(self, value: int) -> None:
        """Set duty cycle as 16-bit value."""
        ...

    @overload
    def duty_ns(self) -> int:
        """Get duty cycle in nanoseconds."""
        ...

    @overload
    def duty_ns(self, value: int) -> None:
        """Set duty cycle in nanoseconds."""
        ...


class UART:
    """UART serial communication."""

    INV_TX: int
    INV_RX: int
    RTS: int
    CTS: int

    def __init__(
        self,
        id: int,
        baudrate: int = 9600,
        bits: int = 8,
        parity: Optional[int] = None,
        stop: int = 1,
        *,
        tx: Optional[Pin] = None,
        rx: Optional[Pin] = None,
        rts: Optional[Pin] = None,
        cts: Optional[Pin] = None,
        txbuf: int = 256,
        rxbuf: int = 256,
        timeout: int = 0,
        timeout_char: int = 0,
        invert: int = 0,
        flow: int = 0
    ) -> None:
        """Create UART interface.

        Args:
            id: UART number (0, 1, or 2 on ESP32)
            baudrate: Baud rate
            bits: Data bits (5-8)
            parity: None, 0 (even), or 1 (odd)
            stop: Stop bits (1 or 2)
            tx: TX pin
            rx: RX pin
            rts: RTS pin
            cts: CTS pin
            txbuf: TX buffer size
            rxbuf: RX buffer size
            timeout: Read timeout in ms
            timeout_char: Timeout between characters
            invert: Invert signals (INV_TX, INV_RX)
            flow: Hardware flow control (RTS, CTS)
        """
        ...

    def init(
        self,
        baudrate: int = 9600,
        bits: int = 8,
        parity: Optional[int] = None,
        stop: int = 1,
        **kwargs: Any
    ) -> None:
        """Reinitialize UART."""
        ...

    def deinit(self) -> None:
        """Disable UART."""
        ...

    def any(self) -> int:
        """Return number of bytes waiting in RX buffer."""
        ...

    def read(self, nbytes: Optional[int] = None) -> Optional[bytes]:
        """Read bytes from UART."""
        ...

    def readinto(self, buf: bytearray, nbytes: Optional[int] = None) -> Optional[int]:
        """Read bytes into a buffer."""
        ...

    def readline(self) -> Optional[bytes]:
        """Read a line from UART."""
        ...

    def write(self, buf: bytes) -> Optional[int]:
        """Write bytes to UART."""
        ...

    def sendbreak(self) -> None:
        """Send a break condition."""
        ...

    def flush(self) -> None:
        """Wait until all data is sent."""
        ...

    def txdone(self) -> bool:
        """Return True if all data has been sent."""
        ...


class SPI:
    """Hardware SPI interface."""

    CONTROLLER: int
    MSB: int
    LSB: int

    def __init__(
        self,
        id: int,
        baudrate: int = 1000000,
        *,
        polarity: int = 0,
        phase: int = 0,
        bits: int = 8,
        firstbit: int = MSB,
        sck: Optional[Pin] = None,
        mosi: Optional[Pin] = None,
        miso: Optional[Pin] = None
    ) -> None:
        """Create SPI interface.

        Args:
            id: SPI bus number (1 or 2 on ESP32)
            baudrate: Clock rate in Hz
            polarity: Clock polarity (0 or 1)
            phase: Clock phase (0 or 1)
            bits: Data width (usually 8)
            firstbit: MSB or LSB first
            sck: Clock pin
            mosi: MOSI pin
            miso: MISO pin
        """
        ...

    def init(
        self,
        baudrate: int = 1000000,
        *,
        polarity: int = 0,
        phase: int = 0,
        bits: int = 8,
        firstbit: int = MSB,
        sck: Optional[Pin] = None,
        mosi: Optional[Pin] = None,
        miso: Optional[Pin] = None
    ) -> None:
        """Reinitialize SPI."""
        ...

    def deinit(self) -> None:
        """Disable SPI."""
        ...

    def read(self, nbytes: int, write: int = 0x00) -> bytes:
        """Read bytes while writing a value."""
        ...

    def readinto(self, buf: bytearray, write: int = 0x00) -> None:
        """Read into buffer while writing a value."""
        ...

    def write(self, buf: bytes) -> None:
        """Write bytes to SPI."""
        ...

    def write_readinto(self, write_buf: bytes, read_buf: bytearray) -> None:
        """Simultaneous write and read."""
        ...


class SoftSPI:
    """Software (bit-banged) SPI interface."""

    MSB: int
    LSB: int

    def __init__(
        self,
        baudrate: int = 500000,
        *,
        polarity: int = 0,
        phase: int = 0,
        bits: int = 8,
        firstbit: int = MSB,
        sck: Pin = ...,
        mosi: Pin = ...,
        miso: Pin = ...
    ) -> None:
        """Create software SPI.

        Args:
            baudrate: Clock rate in Hz
            polarity: Clock polarity
            phase: Clock phase
            bits: Data width
            firstbit: MSB or LSB first
            sck: Clock pin (required)
            mosi: MOSI pin (required)
            miso: MISO pin (required)
        """
        ...

    def init(self, **kwargs: Any) -> None: ...
    def deinit(self) -> None: ...
    def read(self, nbytes: int, write: int = 0x00) -> bytes: ...
    def readinto(self, buf: bytearray, write: int = 0x00) -> None: ...
    def write(self, buf: bytes) -> None: ...
    def write_readinto(self, write_buf: bytes, read_buf: bytearray) -> None: ...


class I2C:
    """Hardware I2C interface."""

    def __init__(
        self,
        id: int,
        *,
        scl: Optional[Pin] = None,
        sda: Optional[Pin] = None,
        freq: int = 400000,
        timeout: int = 50000
    ) -> None:
        """Create I2C interface.

        Args:
            id: I2C bus number (0 or 1 on ESP32)
            scl: SCL pin
            sda: SDA pin
            freq: Clock frequency in Hz
            timeout: Timeout in microseconds
        """
        ...

    def init(
        self,
        *,
        scl: Optional[Pin] = None,
        sda: Optional[Pin] = None,
        freq: int = 400000
    ) -> None:
        """Reinitialize I2C."""
        ...

    def deinit(self) -> None:
        """Disable I2C."""
        ...

    def scan(self) -> list[int]:
        """Scan for devices and return list of addresses."""
        ...

    def start(self) -> None:
        """Generate a START condition."""
        ...

    def stop(self) -> None:
        """Generate a STOP condition."""
        ...

    def readinto(self, buf: bytearray, nack: bool = True) -> None:
        """Read bytes into buffer."""
        ...

    def write(self, buf: bytes) -> int:
        """Write bytes and return number of ACKs."""
        ...

    def readfrom(self, addr: int, nbytes: int, stop: bool = True) -> bytes:
        """Read from a device."""
        ...

    def readfrom_into(
        self,
        addr: int,
        buf: bytearray,
        stop: bool = True
    ) -> None:
        """Read from a device into buffer."""
        ...

    def writeto(
        self,
        addr: int,
        buf: bytes,
        stop: bool = True
    ) -> int:
        """Write to a device."""
        ...

    def writevto(
        self,
        addr: int,
        vector: tuple[bytes, ...],
        stop: bool = True
    ) -> int:
        """Write multiple buffers to a device."""
        ...

    def readfrom_mem(
        self,
        addr: int,
        memaddr: int,
        nbytes: int,
        *,
        addrsize: int = 8
    ) -> bytes:
        """Read from a device memory address."""
        ...

    def readfrom_mem_into(
        self,
        addr: int,
        memaddr: int,
        buf: bytearray,
        *,
        addrsize: int = 8
    ) -> None:
        """Read from device memory into buffer."""
        ...

    def writeto_mem(
        self,
        addr: int,
        memaddr: int,
        buf: bytes,
        *,
        addrsize: int = 8
    ) -> None:
        """Write to a device memory address."""
        ...


class SoftI2C:
    """Software (bit-banged) I2C interface."""

    def __init__(
        self,
        scl: Pin,
        sda: Pin,
        *,
        freq: int = 400000,
        timeout: int = 50000
    ) -> None:
        """Create software I2C.

        Args:
            scl: SCL pin (required)
            sda: SDA pin (required)
            freq: Clock frequency in Hz
            timeout: Timeout in microseconds
        """
        ...

    def init(self, *, scl: Optional[Pin] = None, sda: Optional[Pin] = None, freq: int = 400000) -> None: ...
    def deinit(self) -> None: ...
    def scan(self) -> list[int]: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def readinto(self, buf: bytearray, nack: bool = True) -> None: ...
    def write(self, buf: bytes) -> int: ...
    def readfrom(self, addr: int, nbytes: int, stop: bool = True) -> bytes: ...
    def readfrom_into(self, addr: int, buf: bytearray, stop: bool = True) -> None: ...
    def writeto(self, addr: int, buf: bytes, stop: bool = True) -> int: ...
    def writevto(self, addr: int, vector: tuple[bytes, ...], stop: bool = True) -> int: ...
    def readfrom_mem(self, addr: int, memaddr: int, nbytes: int, *, addrsize: int = 8) -> bytes: ...
    def readfrom_mem_into(self, addr: int, memaddr: int, buf: bytearray, *, addrsize: int = 8) -> None: ...
    def writeto_mem(self, addr: int, memaddr: int, buf: bytes, *, addrsize: int = 8) -> None: ...


class Timer:
    """Hardware timer."""

    ONE_SHOT: int
    PERIODIC: int

    def __init__(
        self,
        id: int,
        *,
        mode: int = PERIODIC,
        period: int = -1,
        freq: int = -1,
        callback: Optional[Callable[["Timer"], None]] = None
    ) -> None:
        """Create a timer.

        Args:
            id: Timer number (0-3 on ESP32)
            mode: ONE_SHOT or PERIODIC
            period: Period in milliseconds
            freq: Frequency in Hz (alternative to period)
            callback: Function to call on timer event
        """
        ...

    def init(
        self,
        *,
        mode: int = PERIODIC,
        period: int = -1,
        freq: int = -1,
        callback: Optional[Callable[["Timer"], None]] = None
    ) -> None:
        """Reinitialize the timer."""
        ...

    def deinit(self) -> None:
        """Stop and disable the timer."""
        ...

    def value(self) -> int:
        """Return current timer value."""
        ...


class RTC:
    """Real Time Clock."""

    ALARM0: int

    def __init__(self, id: int = 0) -> None:
        """Create RTC interface.

        Args:
            id: RTC id (usually 0)
        """
        ...

    def init(self, datetime: Tuple[int, ...]) -> None:
        """Initialize RTC with datetime tuple."""
        ...

    def datetime(
        self,
        dt: Optional[Tuple[int, int, int, int, int, int, int, int]] = None
    ) -> Tuple[int, int, int, int, int, int, int, int]:
        """Get or set datetime.

        Tuple format: (year, month, day, weekday, hours, minutes, seconds, subseconds)
        """
        ...

    def memory(self, data: Optional[bytes] = None) -> bytes:
        """Read or write RTC memory (survives deep sleep)."""
        ...

    def alarm(
        self,
        id: int,
        time: Optional[int] = None,
        *,
        repeat: bool = False
    ) -> None:
        """Set an alarm."""
        ...

    def alarm_left(self, id: int = 0) -> int:
        """Return milliseconds until alarm."""
        ...

    def cancel(self, id: int = 0) -> None:
        """Cancel an alarm."""
        ...

    def irq(
        self,
        *,
        trigger: int,
        handler: Optional[Callable[..., None]] = None,
        wake: int = ...
    ) -> None:
        """Configure RTC interrupt."""
        ...


class WDT:
    """Watchdog Timer."""

    def __init__(self, id: int = 0, timeout: int = 5000) -> None:
        """Create watchdog timer.

        Args:
            id: WDT id (usually 0)
            timeout: Timeout in milliseconds
        """
        ...

    def feed(self) -> None:
        """Feed the watchdog to prevent reset."""
        ...


class TouchPad:
    """Touch sensor (ESP32)."""

    def __init__(self, pin: Pin) -> None:
        """Create TouchPad on a touch-capable pin.

        Args:
            pin: Touch-capable pin (GPIO 0, 2, 4, 12-15, 27, 32, 33)
        """
        ...

    def read(self) -> int:
        """Read touch value (lower = touched)."""
        ...

    def config(self, value: int) -> None:
        """Configure touch threshold for wake."""
        ...


class SDCard:
    """SD Card interface."""

    def __init__(
        self,
        slot: int = 1,
        width: int = 1,
        cd: Optional[Pin] = None,
        wp: Optional[Pin] = None,
        sck: Optional[Pin] = None,
        miso: Optional[Pin] = None,
        mosi: Optional[Pin] = None,
        cs: Optional[Pin] = None,
        freq: int = 20000000
    ) -> None:
        """Create SD Card interface.

        Args:
            slot: SD card slot (1 for SPI mode)
            width: Bus width (1 or 4)
            cd: Card detect pin
            wp: Write protect pin
            sck: SPI clock pin
            miso: SPI MISO pin
            mosi: SPI MOSI pin
            cs: SPI chip select pin
            freq: SPI frequency
        """
        ...

    def info(self) -> Tuple[int, int]:
        """Return (block_count, block_size)."""
        ...

    def readblocks(self, block_num: int, buf: bytearray) -> None:
        """Read blocks into buffer."""
        ...

    def writeblocks(self, block_num: int, buf: bytes) -> None:
        """Write blocks from buffer."""
        ...

    def ioctl(self, cmd: int, arg: Any = None) -> Any:
        """Control the SD card."""
        ...
