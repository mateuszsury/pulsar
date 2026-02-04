"""Type stubs for MicroPython espnow module (ESP-NOW protocol)."""

from typing import Any, Callable, Iterator, Optional, Tuple, Union


class ESPNow:
    """ESP-NOW wireless communication protocol.

    ESP-NOW allows direct device-to-device communication without WiFi AP.
    Maximum payload is 250 bytes.
    """

    MAX_DATA_LEN: int  # 250 bytes
    KEY_LEN: int  # 16 bytes
    MAX_TOTAL_PEER_NUM: int  # Usually 20
    MAX_ENCRYPT_PEER_NUM: int  # Usually 6

    def __init__(self) -> None:
        """Create ESP-NOW interface."""
        ...

    def active(self, flag: Optional[bool] = None) -> bool:
        """Get or set ESP-NOW active state.

        Args:
            flag: True to activate, False to deactivate, None to query

        Returns:
            Current active state
        """
        ...

    def config(self, **kwargs: Any) -> Any:
        """Get or set ESP-NOW configuration.

        Parameters:
            rxbuf: Size of internal rx buffer (default 526 bytes)
            timeout_ms: Timeout for send/recv operations
            rate: WiFi PHY rate for ESP-NOW
        """
        ...

    # Peer management
    def add_peer(
        self,
        mac: bytes,
        lmk: Optional[bytes] = None,
        channel: int = 0,
        ifidx: int = 0,
        encrypt: bool = False
    ) -> None:
        """Add a peer device.

        Args:
            mac: 6-byte MAC address
            lmk: 16-byte Local Master Key for encryption
            channel: WiFi channel (0 = current channel)
            ifidx: WiFi interface (0 = STA, 1 = AP)
            encrypt: Enable encryption for this peer
        """
        ...

    def del_peer(self, mac: bytes) -> None:
        """Remove a peer device.

        Args:
            mac: 6-byte MAC address
        """
        ...

    def mod_peer(
        self,
        mac: bytes,
        lmk: Optional[bytes] = None,
        channel: Optional[int] = None,
        ifidx: Optional[int] = None,
        encrypt: Optional[bool] = None
    ) -> None:
        """Modify peer settings."""
        ...

    def get_peer(self, mac: bytes) -> Tuple[bytes, bytes, int, int, bool]:
        """Get peer info.

        Returns:
            Tuple of (mac, lmk, channel, ifidx, encrypt)
        """
        ...

    def get_peers(self) -> Tuple[Tuple[bytes, bytes, int, int, bool], ...]:
        """Get all registered peers."""
        ...

    def peers_table(self) -> dict[bytes, list[Any]]:
        """Get peer statistics table."""
        ...

    # Sending data
    def send(
        self,
        mac: Optional[bytes],
        msg: Union[bytes, str],
        sync: bool = True
    ) -> bool:
        """Send data to a peer.

        Args:
            mac: Destination MAC (None for broadcast)
            msg: Data to send (max 250 bytes)
            sync: Wait for confirmation

        Returns:
            True if successful
        """
        ...

    # Receiving data
    def recv(self, timeout_ms: Optional[int] = None) -> Tuple[Optional[bytes], Optional[bytes]]:
        """Receive data from any peer.

        Args:
            timeout_ms: Receive timeout (None = use config timeout)

        Returns:
            Tuple of (mac, msg) or (None, None) on timeout
        """
        ...

    def recvinto(
        self,
        data: bytearray,
        timeout_ms: Optional[int] = None
    ) -> Tuple[Optional[bytes], int]:
        """Receive data into existing buffer.

        Args:
            data: Buffer to receive into
            timeout_ms: Receive timeout

        Returns:
            Tuple of (mac, length) or (None, 0) on timeout
        """
        ...

    def irecv(self, timeout_ms: Optional[int] = None) -> Tuple[Optional[bytes], Optional[bytes]]:
        """Receive data (iterator-friendly, returns same buffer).

        Use this in loops for memory efficiency.
        """
        ...

    def any(self) -> bool:
        """Check if data is available to receive."""
        ...

    def __iter__(self) -> Iterator[Tuple[bytes, bytes]]:
        """Iterate over received messages."""
        ...

    def __next__(self) -> Tuple[bytes, bytes]:
        """Get next received message."""
        ...

    # Callbacks
    def irq(self, callback: Optional[Callable[["ESPNow"], None]]) -> None:
        """Set callback for received data.

        Args:
            callback: Function called when data received
        """
        ...

    # Statistics
    def stats(self) -> Tuple[int, int, int, int, int]:
        """Get ESP-NOW statistics.

        Returns:
            Tuple of (tx_pkts, tx_responses, tx_failures, rx_pkts, rx_dropped)
        """
        ...

    # Buffer management
    def set_pmk(self, pmk: bytes) -> None:
        """Set Primary Master Key for encryption.

        Args:
            pmk: 16-byte Primary Master Key
        """
        ...


class ESPNowConnection:
    """Helper class for ESP-NOW connections (from aioespnow)."""

    def __init__(self, espnow: ESPNow, mac: bytes) -> None:
        """Create connection to specific peer."""
        ...

    async def send(self, msg: bytes) -> bool:
        """Send message to this peer."""
        ...

    async def recv(self) -> bytes:
        """Receive message from this peer."""
        ...
