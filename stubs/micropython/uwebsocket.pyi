"""Type stubs for uwebsocket module (WebSocket client/server)."""

from typing import Any, Optional, Union


class websocket:
    """WebSocket connection.

    Example client:
        import uwebsocket
        import usocket

        sock = usocket.socket()
        sock.connect(('echo.websocket.org', 80))

        ws = uwebsocket.websocket(sock)
        ws.send('Hello')
        msg = ws.recv()
        print(msg)
        ws.close()
    """

    def __init__(self, sock: Any, is_client: bool = True) -> None:
        """Create WebSocket.

        Args:
            sock: Underlying socket
            is_client: True for client, False for server
        """
        ...

    def send(self, data: Union[str, bytes]) -> None:
        """Send message.

        Args:
            data: String or bytes to send
        """
        ...

    def recv(self) -> Union[str, bytes]:
        """Receive message.

        Returns:
            Received string or bytes
        """
        ...

    def close(self, code: int = 1000, reason: str = "") -> None:
        """Close connection.

        Args:
            code: Close code (1000 = normal)
            reason: Close reason text
        """
        ...

    def ping(self, data: bytes = b"") -> None:
        """Send ping frame."""
        ...

    def pong(self, data: bytes = b"") -> None:
        """Send pong frame."""
        ...


def connect(url: str, headers: Optional[dict] = None) -> websocket:
    """Connect to WebSocket server.

    Args:
        url: WebSocket URL (ws:// or wss://)
        headers: Additional HTTP headers

    Returns:
        WebSocket connection

    Example:
        import uwebsocket

        ws = uwebsocket.connect('ws://echo.websocket.org')
        ws.send('Hello')
        print(ws.recv())
        ws.close()
    """
    ...


class WebSocketClient:
    """Async WebSocket client.

    Example:
        import uasyncio
        from uwebsocket import WebSocketClient

        async def main():
            ws = WebSocketClient('ws://echo.websocket.org')
            await ws.connect()
            await ws.send('Hello')
            msg = await ws.recv()
            print(msg)
            await ws.close()

        uasyncio.run(main())
    """

    def __init__(
        self,
        url: str,
        headers: Optional[dict] = None,
        ssl: bool = False
    ) -> None:
        """Create async WebSocket client.

        Args:
            url: WebSocket URL
            headers: Additional HTTP headers
            ssl: Enable SSL/TLS
        """
        ...

    async def connect(self) -> None:
        """Connect to server."""
        ...

    async def send(self, data: Union[str, bytes]) -> None:
        """Send message."""
        ...

    async def recv(self) -> Union[str, bytes]:
        """Receive message."""
        ...

    async def close(self) -> None:
        """Close connection."""
        ...

    def is_connected(self) -> bool:
        """Check if connected."""
        ...
