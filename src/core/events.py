"""Event bus for pub/sub communication between components."""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Coroutine, TypeAlias

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of events in the system."""

    # Device events
    DEVICE_DISCOVERED = auto()
    DEVICE_CONNECTED = auto()
    DEVICE_DISCONNECTED = auto()
    DEVICE_ERROR = auto()
    DEVICE_OUTPUT = auto()

    # Port events
    PORTS_UPDATED = auto()

    # File events
    FILE_PROGRESS = auto()
    FILE_UPLOADED = auto()
    FILE_DOWNLOADED = auto()
    FILE_DELETED = auto()

    # REPL events
    REPL_INPUT = auto()
    REPL_OUTPUT = auto()
    REPL_ERROR = auto()

    # Control events (reset, interrupt)
    DEVICE_RESET = auto()
    DEVICE_INTERRUPTED = auto()

    # Firmware events
    FIRMWARE_PROGRESS = auto()
    FIRMWARE_COMPLETE = auto()
    FIRMWARE_ERROR = auto()

    # WiFi events
    WIFI_SCAN_RESULT = auto()
    WIFI_CONNECTED = auto()
    WIFI_DISCONNECTED = auto()

    # Application events
    APP_READY = auto()
    APP_SHUTDOWN = auto()
    CONFIG_CHANGED = auto()

    # LSP events
    LSP_INITIALIZED = auto()
    LSP_DIAGNOSTICS = auto()
    LSP_ERROR = auto()
    LSP_SHUTDOWN = auto()


@dataclass
class Event:
    """Event data container."""

    type: EventType
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert event to dictionary for JSON serialization."""
        # Convert DEVICE_OUTPUT to device:output format for frontend compatibility
        type_name = self.type.name.lower()
        # Replace first underscore with colon for category:action format
        if "_" in type_name:
            parts = type_name.split("_", 1)
            type_name = f"{parts[0]}:{parts[1]}"
        return {
            "type": type_name,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
        }


EventHandler: TypeAlias = Callable[[Event], Coroutine[Any, Any, None]]


class EventBus:
    """Async event bus for pub/sub communication."""

    def __init__(self) -> None:
        self._handlers: dict[EventType, list[EventHandler]] = {}
        self._global_handlers: list[EventHandler] = []
        self._queue: asyncio.Queue[Event] = asyncio.Queue()
        self._running = False
        self._task: asyncio.Task[None] | None = None

    def subscribe(
        self,
        event_type: EventType | None,
        handler: EventHandler,
    ) -> Callable[[], None]:
        """
        Subscribe to an event type.

        Args:
            event_type: Event type to subscribe to, or None for all events.
            handler: Async function to call when event is published.

        Returns:
            Unsubscribe function.
        """
        if event_type is None:
            self._global_handlers.append(handler)
            return lambda: self._global_handlers.remove(handler)

        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

        def unsubscribe() -> None:
            if event_type in self._handlers:
                self._handlers[event_type].remove(handler)

        return unsubscribe

    def publish(self, event: Event) -> None:
        """
        Publish an event to all subscribers.

        Args:
            event: Event to publish.
        """
        self._queue.put_nowait(event)
        logger.debug("Published event: %s", event.type.name)

    def emit(
        self,
        event_type: EventType,
        data: dict[str, Any] | None = None,
        source: str = "",
    ) -> None:
        """
        Convenience method to emit an event.

        Args:
            event_type: Type of event.
            data: Event data.
            source: Source identifier.
        """
        self.publish(Event(
            type=event_type,
            data=data or {},
            source=source,
        ))

    async def start(self) -> None:
        """Start the event processing loop."""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._process_events())
        logger.info("Event bus started")

    async def stop(self) -> None:
        """Stop the event processing loop."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Event bus stopped")

    async def _process_events(self) -> None:
        """Process events from the queue."""
        while self._running:
            try:
                event = await asyncio.wait_for(
                    self._queue.get(),
                    timeout=0.1,
                )
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

            # Call type-specific handlers
            handlers = self._handlers.get(event.type, [])
            for handler in handlers:
                try:
                    await handler(event)
                except Exception as e:
                    logger.exception("Handler error for %s: %s", event.type.name, e)

            # Call global handlers
            for handler in self._global_handlers:
                try:
                    await handler(event)
                except Exception as e:
                    logger.exception("Global handler error: %s", e)
