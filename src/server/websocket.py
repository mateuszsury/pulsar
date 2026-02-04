"""WebSocket handler for real-time communication."""

import asyncio
import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Set
from weakref import WeakSet

from aiohttp import web, WSMsgType

if TYPE_CHECKING:
    from core.events import Event, EventBus
    from serial_comm.manager import SerialManager
    from lsp.manager import LSPManager

logger = logging.getLogger(__name__)


class WebSocketHandler:
    """Handles WebSocket connections and message routing."""

    def __init__(
        self,
        events: "EventBus",
        serial_manager: "SerialManager",
    ) -> None:
        self.events = events
        self.serial_manager = serial_manager

        self._connections: WeakSet[web.WebSocketResponse] = WeakSet()
        self._subscriptions: dict[web.WebSocketResponse, set[str]] = {}
        self._unsubscribe: Any = None

        # LSP manager (lazy-loaded)
        self._lsp_manager: Optional["LSPManager"] = None
        self._lsp_initialized = False

    async def start(self) -> None:
        """Start WebSocket handler."""
        # Subscribe to all events for broadcasting
        self._unsubscribe = self.events.subscribe(None, self._on_event)
        logger.info("WebSocket handler started")

    async def stop(self) -> None:
        """Stop WebSocket handler."""
        if self._unsubscribe:
            self._unsubscribe()

        # Shutdown LSP if running
        if self._lsp_manager:
            await self._lsp_manager.shutdown()
            self._lsp_manager = None
            self._lsp_initialized = False

        # Close all connections
        for ws in list(self._connections):
            try:
                await ws.close()
            except Exception:
                pass

        logger.info("WebSocket handler stopped")

    async def handle(self, request: web.Request) -> web.WebSocketResponse:
        """Handle incoming WebSocket connection."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        self._connections.add(ws)
        self._subscriptions[ws] = set()

        logger.info("WebSocket client connected")

        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    await self._handle_message(ws, msg.data)
                elif msg.type == WSMsgType.ERROR:
                    logger.error("WebSocket error: %s", ws.exception())
                    break

        except Exception as e:
            logger.exception("WebSocket handler error: %s", e)

        finally:
            self._connections.discard(ws)
            self._subscriptions.pop(ws, None)
            logger.info("WebSocket client disconnected")

        return ws

    async def _handle_message(
        self,
        ws: web.WebSocketResponse,
        data: str,
    ) -> None:
        """Handle incoming WebSocket message."""
        try:
            message = json.loads(data)
            msg_type = message.get("type", "")

            if msg_type == "subscribe":
                # Subscribe to device events
                port = message.get("port")
                if port:
                    self._subscriptions[ws].add(port)
                    logger.debug("Client subscribed to %s", port)

            elif msg_type == "unsubscribe":
                # Unsubscribe from device events
                port = message.get("port")
                if port:
                    self._subscriptions[ws].discard(port)
                    logger.debug("Client unsubscribed from %s", port)

            elif msg_type == "repl:input":
                # Send input to device REPL
                port = message.get("port")
                text = message.get("text", "")
                if port and text:
                    device = self.serial_manager.get_device(port)
                    if device:
                        await device.write_line(text)

            elif msg_type == "ping":
                # Respond to ping
                await ws.send_json({"type": "pong"})

            # LSP message types
            elif msg_type == "lsp:initialize":
                await self._handle_lsp_initialize(ws, message)

            elif msg_type == "lsp:request":
                await self._handle_lsp_request(ws, message)

            elif msg_type == "lsp:notification":
                await self._handle_lsp_notification(ws, message)

            elif msg_type == "lsp:shutdown":
                await self._handle_lsp_shutdown(ws)

            else:
                logger.warning("Unknown WebSocket message type: %s", msg_type)

        except json.JSONDecodeError:
            logger.warning("Invalid JSON in WebSocket message")
        except Exception as e:
            logger.exception("Error handling WebSocket message: %s", e)

    async def _on_event(self, event: "Event") -> None:
        """Handle events and broadcast to clients."""
        event_data = event.to_dict()

        # Get port from event source
        port = event.source

        logger.debug("Broadcasting event: %s (port=%s)", event.type.name, port)

        for ws in list(self._connections):
            try:
                # Check if client is subscribed to this port
                subs = self._subscriptions.get(ws, set())

                # Send if no subscriptions (global) or subscribed to this port
                if not subs or port in subs or not port:
                    logger.debug("Sending to client (subs=%s)", subs)
                    await ws.send_json(event_data)

            except Exception as e:
                logger.debug("Failed to send to WebSocket: %s", e)
                self._connections.discard(ws)

    async def broadcast(self, data: dict[str, Any]) -> None:
        """Broadcast message to all connected clients."""
        for ws in list(self._connections):
            try:
                await ws.send_json(data)
            except Exception:
                self._connections.discard(ws)

    # LSP Handler Methods

    async def _get_lsp_manager(self) -> "LSPManager":
        """Get or create LSP manager."""
        if self._lsp_manager is None:
            from lsp.manager import LSPManager

            def on_diagnostics(uri: str, diagnostics: list[dict[str, Any]]) -> None:
                # Broadcast diagnostics to all connected clients
                asyncio.create_task(
                    self.broadcast({
                        "type": "lsp:diagnostics",
                        "data": {"uri": uri, "diagnostics": diagnostics},
                    })
                )

            self._lsp_manager = LSPManager(on_diagnostics=on_diagnostics)

        return self._lsp_manager

    async def _handle_lsp_initialize(
        self,
        ws: web.WebSocketResponse,
        message: dict[str, Any],
    ) -> None:
        """Handle LSP initialization request."""
        try:
            lsp = await self._get_lsp_manager()

            # Start LSP if not running
            if not lsp.is_running:
                workspace_root = message.get("workspaceRoot")
                success = await lsp.start(
                    Path(workspace_root) if workspace_root else None
                )
                if not success:
                    await ws.send_json({
                        "type": "lsp:error",
                        "data": {"message": "Failed to start Pyright LSP"},
                    })
                    return

            # Initialize session
            root_uri = message.get("rootUri", "file:///")
            if not lsp.is_initialized:
                result = await lsp.initialize(root_uri)
                self._lsp_initialized = True

                await ws.send_json({
                    "type": "lsp:initialized",
                    "data": {"capabilities": result.get("capabilities", {})},
                })
            else:
                await ws.send_json({
                    "type": "lsp:initialized",
                    "data": {"capabilities": {}},
                })

        except Exception as e:
            logger.exception("LSP initialize error: %s", e)
            await ws.send_json({
                "type": "lsp:error",
                "data": {"message": str(e)},
            })

    async def _handle_lsp_request(
        self,
        ws: web.WebSocketResponse,
        message: dict[str, Any],
    ) -> None:
        """Handle LSP request (completion, hover, definition, etc.)."""
        try:
            lsp = await self._get_lsp_manager()

            if not lsp.is_initialized:
                await ws.send_json({
                    "type": "lsp:error",
                    "data": {"message": "LSP not initialized"},
                })
                return

            method = message.get("method", "")
            params = message.get("params", {})
            request_id = message.get("requestId")

            result: Any = None

            if method == "textDocument/completion":
                uri = params.get("uri", "")
                line = params.get("line", 0)
                character = params.get("character", 0)
                result = await lsp.completion(uri, line, character)

            elif method == "textDocument/hover":
                uri = params.get("uri", "")
                line = params.get("line", 0)
                character = params.get("character", 0)
                result = await lsp.hover(uri, line, character)

            elif method == "textDocument/definition":
                uri = params.get("uri", "")
                line = params.get("line", 0)
                character = params.get("character", 0)
                result = await lsp.definition(uri, line, character)

            elif method == "textDocument/signatureHelp":
                uri = params.get("uri", "")
                line = params.get("line", 0)
                character = params.get("character", 0)
                result = await lsp.signature_help(uri, line, character)

            else:
                logger.warning("Unknown LSP method: %s", method)

            await ws.send_json({
                "type": "lsp:response",
                "data": {
                    "requestId": request_id,
                    "method": method,
                    "result": result,
                },
            })

        except Exception as e:
            logger.exception("LSP request error: %s", e)
            await ws.send_json({
                "type": "lsp:error",
                "data": {
                    "requestId": message.get("requestId"),
                    "message": str(e),
                },
            })

    async def _handle_lsp_notification(
        self,
        ws: web.WebSocketResponse,
        message: dict[str, Any],
    ) -> None:
        """Handle LSP notification (didOpen, didChange, didClose)."""
        try:
            lsp = await self._get_lsp_manager()

            if not lsp.is_initialized:
                return

            method = message.get("method", "")
            params = message.get("params", {})

            if method == "textDocument/didOpen":
                uri = params.get("uri", "")
                content = params.get("content", "")
                language_id = params.get("languageId", "python")
                await lsp.did_open(uri, content, language_id)

            elif method == "textDocument/didChange":
                uri = params.get("uri", "")
                content = params.get("content", "")
                version = params.get("version", 1)
                await lsp.did_change(uri, content, version)

            elif method == "textDocument/didClose":
                uri = params.get("uri", "")
                await lsp.did_close(uri)

            else:
                logger.debug("Unhandled LSP notification: %s", method)

        except Exception as e:
            logger.exception("LSP notification error: %s", e)

    async def _handle_lsp_shutdown(self, ws: web.WebSocketResponse) -> None:
        """Handle LSP shutdown request."""
        try:
            if self._lsp_manager:
                await self._lsp_manager.shutdown()
                self._lsp_manager = None
                self._lsp_initialized = False

            await ws.send_json({
                "type": "lsp:shutdown",
                "data": {"success": True},
            })

        except Exception as e:
            logger.exception("LSP shutdown error: %s", e)
            await ws.send_json({
                "type": "lsp:error",
                "data": {"message": str(e)},
            })
