"""Type stubs for umqtt.simple module (MQTT client)."""

from typing import Any, Callable, Optional, Tuple, Union


class MQTTException(Exception):
    """MQTT protocol exception."""
    pass


class MQTTClient:
    """Simple MQTT client for MicroPython.

    Example:
        from umqtt.simple import MQTTClient

        def callback(topic, msg):
            print(f"Received: {topic} -> {msg}")

        client = MQTTClient("esp32", "broker.hivemq.com")
        client.set_callback(callback)
        client.connect()
        client.subscribe(b"test/topic")

        while True:
            client.check_msg()
    """

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
        """Create MQTT client.

        Args:
            client_id: Unique client identifier
            server: MQTT broker hostname/IP
            port: Broker port (default: 1883 or 8883 for SSL)
            user: Username for authentication
            password: Password for authentication
            keepalive: Keep-alive interval in seconds (0 = disabled)
            ssl: Enable SSL/TLS
            ssl_params: SSL parameters dict
        """
        ...

    def set_callback(
        self,
        callback: Callable[[bytes, bytes], None]
    ) -> None:
        """Set callback for received messages.

        Args:
            callback: Function(topic, message) called on message receipt
        """
        ...

    def set_last_will(
        self,
        topic: Union[str, bytes],
        msg: Union[str, bytes],
        retain: bool = False,
        qos: int = 0
    ) -> None:
        """Set last will message (sent if connection lost).

        Args:
            topic: Will topic
            msg: Will message
            retain: Retain flag
            qos: QoS level (0, 1, or 2)

        Note:
            Must be called before connect().
        """
        ...

    def connect(self, clean_session: bool = True) -> int:
        """Connect to MQTT broker.

        Args:
            clean_session: Start fresh session (discard queued messages)

        Returns:
            0 on success

        Raises:
            MQTTException: On connection failure
        """
        ...

    def disconnect(self) -> None:
        """Disconnect from broker."""
        ...

    def ping(self) -> None:
        """Send MQTT PINGREQ to keep connection alive."""
        ...

    def publish(
        self,
        topic: Union[str, bytes],
        msg: Union[str, bytes],
        retain: bool = False,
        qos: int = 0
    ) -> None:
        """Publish message to topic.

        Args:
            topic: Topic to publish to
            msg: Message payload
            retain: Retain message on broker
            qos: Quality of Service (0, 1, or 2)
        """
        ...

    def subscribe(
        self,
        topic: Union[str, bytes],
        qos: int = 0
    ) -> None:
        """Subscribe to topic.

        Args:
            topic: Topic pattern (supports wildcards + and #)
            qos: Maximum QoS level for messages
        """
        ...

    def wait_msg(self) -> None:
        """Wait for a message (blocking).

        Blocks until a message is received, then calls callback.
        """
        ...

    def check_msg(self) -> None:
        """Check for pending message (non-blocking).

        If a message is available, calls callback.
        Returns immediately if no message.
        """
        ...
