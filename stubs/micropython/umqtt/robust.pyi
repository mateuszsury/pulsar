"""Type stubs for umqtt.robust module (robust MQTT client)."""

from typing import Any, Callable, Optional, Union
from umqtt.simple import MQTTClient as SimpleMQTTClient


class MQTTClient(SimpleMQTTClient):
    """Robust MQTT client with auto-reconnection.

    Extends simple client with automatic reconnection on failures.

    Example:
        from umqtt.robust import MQTTClient

        client = MQTTClient("esp32", "broker.hivemq.com")
        client.connect()

        # Will automatically reconnect if connection lost
        client.publish(b"test/topic", b"Hello")
    """

    DELAY: int  # Reconnection delay in seconds (default: 2)
    DEBUG: bool  # Enable debug output

    def __init__(
        self,
        client_id: Union[str, bytes],
        server: str,
        port: int = 0,
        user: Optional[Union[str, bytes]] = None,
        password: Optional[Union[str, bytes]] = None,
        keepalive: int = 0,
        ssl: bool = False,
        ssl_params: Optional[dict] = None
    ) -> None:
        """Create robust MQTT client.

        Same parameters as simple client.
        """
        ...

    def delay(self, i: int) -> None:
        """Set reconnection delay.

        Args:
            i: Delay in seconds
        """
        ...

    def log(self, in_reconnect: bool, e: Exception) -> None:
        """Log reconnection attempts.

        Override this method for custom logging.

        Args:
            in_reconnect: True if currently reconnecting
            e: Exception that triggered reconnection
        """
        ...

    def reconnect(self) -> None:
        """Reconnect to broker.

        Called automatically on connection failures.
        Can also be called manually.
        """
        ...

    def publish(
        self,
        topic: Union[str, bytes],
        msg: Union[str, bytes],
        retain: bool = False,
        qos: int = 0
    ) -> None:
        """Publish with auto-reconnect.

        Same as simple publish but reconnects on failure.
        """
        ...

    def wait_msg(self) -> None:
        """Wait for message with auto-reconnect."""
        ...

    def check_msg(self) -> None:
        """Check for message with auto-reconnect."""
        ...
