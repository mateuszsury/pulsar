"""Main application class."""

import asyncio
import logging
import threading
from typing import Any

from core.config import Config
from core.events import EventBus, EventType

logger = logging.getLogger(__name__)


class Application:
    """Main application orchestrator."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.events = EventBus()

        # Components (initialized in setup)
        self._serial_manager: Any = None
        self._server: Any = None
        self._window: Any = None

        self._loop: asyncio.AbstractEventLoop | None = None
        self._shutdown_event: asyncio.Event | None = None

    async def _async_setup(self) -> None:
        """Initialize all application components asynchronously."""
        logger.info("Setting up application components...")

        self._shutdown_event = asyncio.Event()

        # Start event bus
        await self.events.start()

        # Initialize serial manager
        from serial_comm.manager import SerialManager
        self._serial_manager = SerialManager(self.events, self.config)
        await self._serial_manager.start()

        # Initialize HTTP/WebSocket server
        from server.api import APIServer
        self._server = APIServer(
            events=self.events,
            config=self.config,
            serial_manager=self._serial_manager,
        )
        await self._server.start()

        # Emit ready event
        self.events.emit(EventType.APP_READY, {"config": self.config.__dict__})
        logger.info("Application ready")

    async def _async_shutdown(self) -> None:
        """Cleanup and shutdown all components."""
        logger.info("Shutting down application...")

        self.events.emit(EventType.APP_SHUTDOWN)

        # Stop components in reverse order
        if self._server:
            await self._server.stop()

        if self._serial_manager:
            await self._serial_manager.stop()

        await self.events.stop()

        # Save config
        self.config.save()

        logger.info("Application shutdown complete")

    def _run_async_loop(self) -> None:
        """Run the async event loop in a separate thread."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        try:
            # Setup components
            self._loop.run_until_complete(self._async_setup())

            # Wait for shutdown signal
            self._loop.run_until_complete(self._shutdown_event.wait())

            # Cleanup
            self._loop.run_until_complete(self._async_shutdown())
        finally:
            self._loop.close()

    def _trigger_shutdown(self) -> None:
        """Trigger shutdown from main thread."""
        if self._loop and self._shutdown_event:
            self._loop.call_soon_threadsafe(self._shutdown_event.set)

    def run(self) -> None:
        """Run the application."""
        if self.config.headless:
            # Run without window - just use asyncio
            asyncio.run(self._run_headless())
        else:
            # Run with pywebview on main thread
            self._run_with_window()

    async def _run_headless(self) -> None:
        """Run in headless mode (no window)."""
        self._shutdown_event = asyncio.Event()

        await self._async_setup()

        logger.info(
            "Running in headless mode. API available at http://%s:%d",
            self.config.server_host,
            self.config.server_port,
        )

        try:
            await self._shutdown_event.wait()
        except KeyboardInterrupt:
            pass
        finally:
            await self._async_shutdown()

    def _run_with_window(self) -> None:
        """Run with pywebview on main thread."""
        import webview

        # Start async loop in background thread
        async_thread = threading.Thread(target=self._run_async_loop, daemon=True)
        async_thread.start()

        # Wait a bit for server to start
        import time
        time.sleep(0.5)

        # Create window (must be on main thread)
        from ui.window import create_window
        self._window = create_window(self.config)

        logger.info("Starting pywebview...")

        # Run webview on main thread (blocking)
        webview.start(debug=self.config.debug)

        # Window closed, trigger shutdown
        self._trigger_shutdown()

        # Wait for async thread to finish
        async_thread.join(timeout=5.0)
