"""Type stubs for MicroPython usocket module (socket networking)."""

from typing import Any, Optional, Tuple, Union

# Address families
AF_INET: int
AF_INET6: int

# Socket types
SOCK_STREAM: int
SOCK_DGRAM: int
SOCK_RAW: int

# IP protocols
IPPROTO_TCP: int
IPPROTO_UDP: int
IPPROTO_IP: int

# Socket options
SOL_SOCKET: int
SO_REUSEADDR: int
SO_BROADCAST: int
SO_KEEPALIVE: int
SO_LINGER: int
SO_RCVBUF: int
SO_SNDBUF: int
SO_RCVTIMEO: int
SO_SNDTIMEO: int
SO_SETFIB: int
SO_BINDTODEVICE: int

# IP options
IP_ADD_MEMBERSHIP: int
IP_DROP_MEMBERSHIP: int

# TCP options
TCP_NODELAY: int
IPPROTO_SEC: int

AddressInfo = Tuple[int, int, int, str, Tuple[str, int]]

def getaddrinfo(
    host: str,
    port: int,
    af: int = 0,
    type: int = 0,
    proto: int = 0,
    flags: int = 0
) -> list[AddressInfo]:
    """Translate host/port to socket address info.

    Args:
        host: Hostname or IP address
        port: Port number
        af: Address family (AF_INET, AF_INET6)
        type: Socket type (SOCK_STREAM, SOCK_DGRAM)
        proto: Protocol number
        flags: Additional flags

    Returns:
        List of (family, type, proto, canonname, sockaddr) tuples
    """
    ...


class socket:
    """Network socket."""

    def __init__(
        self,
        af: int = AF_INET,
        type: int = SOCK_STREAM,
        proto: int = IPPROTO_TCP
    ) -> None:
        """Create a socket.

        Args:
            af: Address family (AF_INET or AF_INET6)
            type: Socket type (SOCK_STREAM or SOCK_DGRAM)
            proto: Protocol (IPPROTO_TCP or IPPROTO_UDP)
        """
        ...

    def close(self) -> None:
        """Close the socket."""
        ...

    def bind(self, address: Tuple[str, int]) -> None:
        """Bind socket to an address.

        Args:
            address: Tuple of (host, port)
        """
        ...

    def listen(self, backlog: int = 1) -> None:
        """Enable server to accept connections.

        Args:
            backlog: Maximum number of queued connections
        """
        ...

    def accept(self) -> Tuple["socket", Tuple[str, int]]:
        """Accept a connection.

        Returns:
            Tuple of (new_socket, (remote_host, remote_port))
        """
        ...

    def connect(self, address: Tuple[str, int]) -> None:
        """Connect to a remote address.

        Args:
            address: Tuple of (host, port)
        """
        ...

    def send(self, data: bytes) -> int:
        """Send data to the socket.

        Args:
            data: Bytes to send

        Returns:
            Number of bytes sent
        """
        ...

    def sendall(self, data: bytes) -> None:
        """Send all data to the socket.

        Args:
            data: Bytes to send
        """
        ...

    def sendto(self, data: bytes, address: Tuple[str, int]) -> int:
        """Send data to a specific address (UDP).

        Args:
            data: Bytes to send
            address: Destination (host, port)

        Returns:
            Number of bytes sent
        """
        ...

    def recv(self, bufsize: int) -> bytes:
        """Receive data from the socket.

        Args:
            bufsize: Maximum bytes to receive

        Returns:
            Received data
        """
        ...

    def recvfrom(self, bufsize: int) -> Tuple[bytes, Tuple[str, int]]:
        """Receive data and sender address (UDP).

        Args:
            bufsize: Maximum bytes to receive

        Returns:
            Tuple of (data, (host, port))
        """
        ...

    def read(self, size: Optional[int] = None) -> bytes:
        """Read from socket (stream interface).

        Args:
            size: Maximum bytes to read

        Returns:
            Data read
        """
        ...

    def readinto(self, buf: bytearray) -> int:
        """Read into a buffer.

        Args:
            buf: Buffer to read into

        Returns:
            Number of bytes read
        """
        ...

    def readline(self) -> bytes:
        """Read a line from socket.

        Returns:
            Line data
        """
        ...

    def write(self, data: bytes) -> int:
        """Write to socket (stream interface).

        Args:
            data: Data to write

        Returns:
            Number of bytes written
        """
        ...

    def setsockopt(self, level: int, optname: int, value: Union[int, bytes]) -> None:
        """Set socket option.

        Args:
            level: Protocol level (SOL_SOCKET, IPPROTO_TCP, etc.)
            optname: Option name
            value: Option value
        """
        ...

    def settimeout(self, value: Optional[float]) -> None:
        """Set socket timeout.

        Args:
            value: Timeout in seconds (None for blocking, 0 for non-blocking)
        """
        ...

    def setblocking(self, flag: bool) -> None:
        """Set blocking/non-blocking mode.

        Args:
            flag: True for blocking, False for non-blocking
        """
        ...

    def makefile(
        self,
        mode: str = "rb",
        buffering: int = 0
    ) -> Any:
        """Create a file object from socket.

        Args:
            mode: File mode ('r', 'w', 'rb', 'wb')
            buffering: Buffering size

        Returns:
            File-like object
        """
        ...

    def fileno(self) -> int:
        """Get socket file descriptor.

        Returns:
            File descriptor number
        """
        ...
