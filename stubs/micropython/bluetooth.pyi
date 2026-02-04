"""Type stubs for MicroPython bluetooth module (BLE)."""

from typing import Any, Callable, Optional, Tuple, Union

# BLE event codes
_IRQ_CENTRAL_CONNECT: int
_IRQ_CENTRAL_DISCONNECT: int
_IRQ_GATTS_WRITE: int
_IRQ_GATTS_READ_REQUEST: int
_IRQ_SCAN_RESULT: int
_IRQ_SCAN_DONE: int
_IRQ_PERIPHERAL_CONNECT: int
_IRQ_PERIPHERAL_DISCONNECT: int
_IRQ_GATTC_SERVICE_RESULT: int
_IRQ_GATTC_SERVICE_DONE: int
_IRQ_GATTC_CHARACTERISTIC_RESULT: int
_IRQ_GATTC_CHARACTERISTIC_DONE: int
_IRQ_GATTC_DESCRIPTOR_RESULT: int
_IRQ_GATTC_DESCRIPTOR_DONE: int
_IRQ_GATTC_READ_RESULT: int
_IRQ_GATTC_READ_DONE: int
_IRQ_GATTC_WRITE_DONE: int
_IRQ_GATTC_NOTIFY: int
_IRQ_GATTC_INDICATE: int
_IRQ_GATTS_INDICATE_DONE: int
_IRQ_MTU_EXCHANGED: int
_IRQ_L2CAP_ACCEPT: int
_IRQ_L2CAP_CONNECT: int
_IRQ_L2CAP_DISCONNECT: int
_IRQ_L2CAP_RECV: int
_IRQ_L2CAP_SEND_READY: int
_IRQ_CONNECTION_UPDATE: int
_IRQ_ENCRYPTION_UPDATE: int
_IRQ_GET_SECRET: int
_IRQ_SET_SECRET: int

# Advertising flags
_ADV_TYPE_FLAGS: int
_ADV_TYPE_NAME: int
_ADV_TYPE_UUID16_COMPLETE: int
_ADV_TYPE_UUID32_COMPLETE: int
_ADV_TYPE_UUID128_COMPLETE: int
_ADV_TYPE_UUID16_MORE: int
_ADV_TYPE_UUID32_MORE: int
_ADV_TYPE_UUID128_MORE: int
_ADV_TYPE_APPEARANCE: int

# Address types
_ADDR_TYPE_PUBLIC: int
_ADDR_TYPE_RANDOM: int

# Flags
FLAG_READ: int
FLAG_WRITE_NO_RESPONSE: int
FLAG_WRITE: int
FLAG_NOTIFY: int
FLAG_INDICATE: int
FLAG_AUTHENTICATED_SIGNED_WRITE: int
FLAG_AUX_WRITE: int
FLAG_READ_ENCRYPTED: int
FLAG_READ_AUTHENTICATED: int
FLAG_READ_AUTHORIZED: int
FLAG_WRITE_ENCRYPTED: int
FLAG_WRITE_AUTHENTICATED: int
FLAG_WRITE_AUTHORIZED: int


class UUID:
    """Bluetooth UUID."""

    def __init__(self, value: Union[int, str, bytes]) -> None:
        """Create a UUID.

        Args:
            value: 16-bit int, 128-bit hex string, or bytes
        """
        ...


class BLE:
    """Bluetooth Low Energy interface."""

    def __init__(self) -> None:
        """Create BLE interface."""
        ...

    def active(self, active: Optional[bool] = None) -> bool:
        """Get or set BLE active state."""
        ...

    def config(self, *args: Any, **kwargs: Any) -> Any:
        """Get or set BLE configuration.

        Parameters:
            mac: MAC address (read-only)
            addr_mode: Address mode
            gap_name: GAP device name
            rxbuf: RX buffer size
            mtu: Maximum transmission unit
            bond: Enable bonding
            mitm: Enable MITM protection
            io: I/O capabilities
            le_secure: Enable LE Secure Connections
        """
        ...

    def irq(self, handler: Callable[[int, Tuple[Any, ...]], None]) -> None:
        """Register BLE event handler.

        Args:
            handler: Function(event, data) called on BLE events
        """
        ...

    # GAP operations
    def gap_advertise(
        self,
        interval_us: Optional[int],
        adv_data: Optional[bytes] = None,
        *,
        resp_data: Optional[bytes] = None,
        connectable: bool = True
    ) -> None:
        """Start or stop advertising.

        Args:
            interval_us: Advertising interval in microseconds, or None to stop
            adv_data: Advertising data
            resp_data: Scan response data
            connectable: Allow connections
        """
        ...

    def gap_scan(
        self,
        duration_ms: int,
        interval_us: int = 1280000,
        window_us: int = 11250,
        active: bool = False
    ) -> None:
        """Start scanning for devices.

        Args:
            duration_ms: Scan duration (0 = indefinite)
            interval_us: Scan interval
            window_us: Scan window
            active: Active scanning (request scan response)
        """
        ...

    def gap_connect(
        self,
        addr_type: int,
        addr: bytes,
        scan_duration_ms: int = 2000
    ) -> None:
        """Connect to a peripheral.

        Args:
            addr_type: Address type (PUBLIC or RANDOM)
            addr: Device address
            scan_duration_ms: Connection timeout
        """
        ...

    def gap_disconnect(self, conn_handle: int) -> bool:
        """Disconnect from a device."""
        ...

    def gap_pair(self, conn_handle: int) -> bool:
        """Initiate pairing."""
        ...

    def gap_passkey(
        self,
        conn_handle: int,
        action: int,
        passkey: int
    ) -> bool:
        """Respond to passkey request."""
        ...

    # GATT Server operations
    def gatts_register_services(
        self,
        services: Tuple[Tuple[UUID, Tuple[Tuple[UUID, int], ...]], ...]
    ) -> Tuple[Tuple[int, ...], ...]:
        """Register GATT services.

        Args:
            services: Service definitions with characteristics

        Returns:
            Tuple of value handles for each characteristic
        """
        ...

    def gatts_read(self, value_handle: int) -> bytes:
        """Read a local characteristic value."""
        ...

    def gatts_write(
        self,
        value_handle: int,
        data: bytes,
        send_update: bool = False
    ) -> None:
        """Write a local characteristic value.

        Args:
            value_handle: Characteristic handle
            data: Data to write
            send_update: Send notification/indication
        """
        ...

    def gatts_notify(
        self,
        conn_handle: int,
        value_handle: int,
        data: Optional[bytes] = None
    ) -> None:
        """Send notification to connected central."""
        ...

    def gatts_indicate(
        self,
        conn_handle: int,
        value_handle: int
    ) -> None:
        """Send indication to connected central."""
        ...

    def gatts_set_buffer(
        self,
        value_handle: int,
        len: int,
        append: bool = False
    ) -> None:
        """Set buffer size for a characteristic."""
        ...

    # GATT Client operations
    def gattc_discover_services(
        self,
        conn_handle: int,
        uuid: Optional[UUID] = None
    ) -> None:
        """Discover services on a peripheral."""
        ...

    def gattc_discover_characteristics(
        self,
        conn_handle: int,
        start_handle: int,
        end_handle: int,
        uuid: Optional[UUID] = None
    ) -> None:
        """Discover characteristics in a service."""
        ...

    def gattc_discover_descriptors(
        self,
        conn_handle: int,
        start_handle: int,
        end_handle: int
    ) -> None:
        """Discover descriptors for a characteristic."""
        ...

    def gattc_read(self, conn_handle: int, value_handle: int) -> None:
        """Read a remote characteristic value."""
        ...

    def gattc_write(
        self,
        conn_handle: int,
        value_handle: int,
        data: bytes,
        mode: int = 0
    ) -> None:
        """Write to a remote characteristic.

        Args:
            conn_handle: Connection handle
            value_handle: Characteristic handle
            data: Data to write
            mode: 0=write with response, 1=write without response
        """
        ...

    def gattc_exchange_mtu(self, conn_handle: int) -> None:
        """Exchange MTU with peripheral."""
        ...

    # L2CAP Connection-Oriented Channels
    def l2cap_listen(self, psm: int, mtu: int) -> None:
        """Listen for L2CAP connections."""
        ...

    def l2cap_connect(
        self,
        conn_handle: int,
        psm: int,
        mtu: int
    ) -> None:
        """Connect L2CAP channel."""
        ...

    def l2cap_disconnect(self, conn_handle: int, cid: int) -> None:
        """Disconnect L2CAP channel."""
        ...

    def l2cap_send(self, conn_handle: int, cid: int, data: bytes) -> None:
        """Send data over L2CAP channel."""
        ...

    def l2cap_recvinto(
        self,
        conn_handle: int,
        cid: int,
        buf: bytearray
    ) -> int:
        """Receive data from L2CAP channel."""
        ...
