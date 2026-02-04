"""LSP Manager for Pyright language server subprocess management."""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Any, Callable, Optional

from lsp.protocol import JSONRPCProtocol

logger = logging.getLogger(__name__)


class LSPManager:
    """Manages Pyright LSP subprocess.

    Handles starting, stopping, and communicating with the Pyright
    language server for MicroPython development.
    """

    def __init__(
        self,
        on_diagnostics: Optional[Callable[[str, list[dict[str, Any]]], None]] = None,
    ) -> None:
        """Initialize LSP manager.

        Args:
            on_diagnostics: Callback for diagnostics notifications
        """
        self._process: Optional[asyncio.subprocess.Process] = None
        self._request_id = 0
        self._pending_requests: dict[int, asyncio.Future[dict[str, Any]]] = {}
        self._buffer = b""
        self._read_task: Optional[asyncio.Task[None]] = None
        self._initialized = False
        self._on_diagnostics = on_diagnostics
        self._workspace_root: Optional[Path] = None

    def _get_stubs_path(self) -> Path:
        """Get MicroPython stubs path, works in dev and bundled mode.

        Returns:
            Path to the stubs directory
        """
        if getattr(sys, "frozen", False):
            # PyInstaller bundle
            return Path(sys._MEIPASS) / "stubs"  # type: ignore
        else:
            # Development mode
            return Path(__file__).parent.parent.parent / "stubs"

    async def start(self, workspace_root: Optional[Path] = None) -> bool:
        """Start Pyright language server.

        Args:
            workspace_root: Root path of the workspace

        Returns:
            True if started successfully
        """
        if self._process is not None:
            logger.warning("LSP already running")
            return True

        self._workspace_root = workspace_root

        try:
            # Start pyright in language server mode
            self._process = await asyncio.create_subprocess_exec(
                sys.executable,
                "-m",
                "pyright",
                "--langserver",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            # Start response reader
            self._read_task = asyncio.create_task(self._read_responses())

            logger.info("Pyright LSP started (PID: %s)", self._process.pid)
            return True

        except FileNotFoundError:
            logger.error("Pyright not found. Install with: pip install pyright")
            return False
        except Exception as e:
            logger.exception("Failed to start Pyright LSP: %s", e)
            return False

    async def initialize(self, root_uri: str) -> dict[str, Any]:
        """Initialize LSP session.

        Args:
            root_uri: Root URI of the workspace

        Returns:
            Server capabilities
        """
        if self._initialized:
            return {}

        stubs_path = self._get_stubs_path()

        # Initialize request
        result = await self.send_request(
            "initialize",
            {
                "processId": None,
                "rootUri": root_uri,
                "capabilities": {
                    "textDocument": {
                        "completion": {
                            "completionItem": {
                                "snippetSupport": True,
                                "documentationFormat": ["markdown", "plaintext"],
                            },
                        },
                        "hover": {
                            "contentFormat": ["markdown", "plaintext"],
                        },
                        "signatureHelp": {
                            "signatureInformation": {
                                "documentationFormat": ["markdown", "plaintext"],
                            },
                        },
                        "publishDiagnostics": {
                            "relatedInformation": True,
                        },
                    },
                    "workspace": {
                        "configuration": True,
                    },
                },
                "initializationOptions": {
                    "python.analysis.extraPaths": [str(stubs_path / "micropython")],
                    "python.analysis.stubPath": str(stubs_path / "micropython"),
                    "python.analysis.typeCheckingMode": "basic",
                    "python.analysis.diagnosticMode": "openFilesOnly",
                },
            },
        )

        # Send initialized notification
        await self.send_notification("initialized", {})

        self._initialized = True
        logger.info("LSP initialized with capabilities: %s", result.get("capabilities", {}))

        return result

    async def shutdown(self) -> None:
        """Gracefully stop LSP server."""
        if self._process is None:
            return

        try:
            # Send shutdown request
            await self.send_request("shutdown", None, timeout=5.0)

            # Send exit notification
            await self.send_notification("exit", None)

        except Exception as e:
            logger.warning("Error during LSP shutdown: %s", e)

        finally:
            # Cancel read task
            if self._read_task:
                self._read_task.cancel()
                try:
                    await self._read_task
                except asyncio.CancelledError:
                    pass
                self._read_task = None

            # Terminate process
            if self._process:
                try:
                    self._process.terminate()
                    await asyncio.wait_for(self._process.wait(), timeout=5.0)
                except asyncio.TimeoutError:
                    self._process.kill()
                except Exception:
                    pass
                self._process = None

            self._initialized = False
            self._pending_requests.clear()
            logger.info("LSP shut down")

    async def send_request(
        self,
        method: str,
        params: Optional[dict[str, Any]],
        timeout: float = 30.0,
    ) -> dict[str, Any]:
        """Send LSP request and wait for response.

        Args:
            method: LSP method name
            params: Request parameters
            timeout: Response timeout in seconds

        Returns:
            Response result

        Raises:
            TimeoutError: If response not received within timeout
            RuntimeError: If LSP not running or request fails
        """
        if self._process is None or self._process.stdin is None:
            raise RuntimeError("LSP not running")

        # Create request
        self._request_id += 1
        request_id = self._request_id
        request = JSONRPCProtocol.create_request(request_id, method, params)

        # Create future for response
        future: asyncio.Future[dict[str, Any]] = asyncio.Future()
        self._pending_requests[request_id] = future

        try:
            # Send request
            data = JSONRPCProtocol.encode(request)
            self._process.stdin.write(data)
            await self._process.stdin.drain()

            logger.debug("Sent request %d: %s", request_id, method)

            # Wait for response
            result = await asyncio.wait_for(future, timeout=timeout)
            return result

        except asyncio.TimeoutError:
            logger.warning("Request %d timed out: %s", request_id, method)
            raise

        finally:
            self._pending_requests.pop(request_id, None)

    async def send_notification(
        self,
        method: str,
        params: Optional[dict[str, Any]],
    ) -> None:
        """Send LSP notification (no response expected).

        Args:
            method: LSP method name
            params: Notification parameters
        """
        if self._process is None or self._process.stdin is None:
            return

        notification = JSONRPCProtocol.create_notification(method, params)
        data = JSONRPCProtocol.encode(notification)

        self._process.stdin.write(data)
        await self._process.stdin.drain()

        logger.debug("Sent notification: %s", method)

    async def _read_responses(self) -> None:
        """Read and process responses from LSP server."""
        if self._process is None or self._process.stdout is None:
            return

        while True:
            try:
                # Read message
                message = await JSONRPCProtocol.decode(self._process.stdout)
                if message is None:
                    logger.info("LSP connection closed")
                    break

                await self._handle_message(message)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception("Error reading LSP response: %s", e)

    async def _handle_message(self, message: dict[str, Any]) -> None:
        """Handle incoming LSP message.

        Args:
            message: Decoded JSON-RPC message
        """
        if "id" in message:
            # Response to our request
            request_id = message["id"]
            future = self._pending_requests.get(request_id)

            if future and not future.done():
                if "error" in message:
                    error = message["error"]
                    logger.warning(
                        "LSP error %d: %s",
                        error.get("code"),
                        error.get("message"),
                    )
                    future.set_exception(
                        RuntimeError(f"LSP error: {error.get('message')}")
                    )
                else:
                    future.set_result(message.get("result", {}))

        elif "method" in message:
            # Notification from server
            method = message["method"]
            params = message.get("params", {})

            if method == "textDocument/publishDiagnostics":
                # Handle diagnostics
                uri = params.get("uri", "")
                diagnostics = params.get("diagnostics", [])
                logger.debug("Diagnostics for %s: %d items", uri, len(diagnostics))

                if self._on_diagnostics:
                    self._on_diagnostics(uri, diagnostics)

            elif method == "window/logMessage":
                # Log server messages
                msg_type = params.get("type", 4)
                msg = params.get("message", "")
                if msg_type == 1:
                    logger.error("LSP: %s", msg)
                elif msg_type == 2:
                    logger.warning("LSP: %s", msg)
                else:
                    logger.info("LSP: %s", msg)

            else:
                logger.debug("Unhandled notification: %s", method)

    # High-level API methods

    async def did_open(self, uri: str, content: str, language_id: str = "python") -> None:
        """Notify server that a document was opened.

        Args:
            uri: Document URI
            content: Document content
            language_id: Language identifier
        """
        await self.send_notification(
            "textDocument/didOpen",
            {
                "textDocument": {
                    "uri": uri,
                    "languageId": language_id,
                    "version": 1,
                    "text": content,
                },
            },
        )

    async def did_change(self, uri: str, content: str, version: int = 1) -> None:
        """Notify server that a document changed.

        Args:
            uri: Document URI
            content: New document content
            version: Document version
        """
        await self.send_notification(
            "textDocument/didChange",
            {
                "textDocument": {
                    "uri": uri,
                    "version": version,
                },
                "contentChanges": [{"text": content}],
            },
        )

    async def did_close(self, uri: str) -> None:
        """Notify server that a document was closed.

        Args:
            uri: Document URI
        """
        await self.send_notification(
            "textDocument/didClose",
            {
                "textDocument": {"uri": uri},
            },
        )

    async def completion(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[dict[str, Any]]:
        """Get completions at a position.

        Args:
            uri: Document URI
            line: Line number (0-indexed)
            character: Character position (0-indexed)

        Returns:
            List of completion items
        """
        result = await self.send_request(
            "textDocument/completion",
            {
                "textDocument": {"uri": uri},
                "position": {"line": line, "character": character},
            },
        )

        # Handle CompletionList or plain list
        if isinstance(result, dict):
            return result.get("items", [])
        elif isinstance(result, list):
            return result
        return []

    async def hover(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> Optional[dict[str, Any]]:
        """Get hover information at a position.

        Args:
            uri: Document URI
            line: Line number (0-indexed)
            character: Character position (0-indexed)

        Returns:
            Hover information or None
        """
        result = await self.send_request(
            "textDocument/hover",
            {
                "textDocument": {"uri": uri},
                "position": {"line": line, "character": character},
            },
        )

        return result if result else None

    async def definition(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[dict[str, Any]]:
        """Get definition locations.

        Args:
            uri: Document URI
            line: Line number (0-indexed)
            character: Character position (0-indexed)

        Returns:
            List of locations
        """
        result = await self.send_request(
            "textDocument/definition",
            {
                "textDocument": {"uri": uri},
                "position": {"line": line, "character": character},
            },
        )

        if result is None:
            return []
        elif isinstance(result, list):
            return result
        else:
            return [result]

    async def signature_help(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> Optional[dict[str, Any]]:
        """Get signature help at a position.

        Args:
            uri: Document URI
            line: Line number (0-indexed)
            character: Character position (0-indexed)

        Returns:
            Signature help or None
        """
        result = await self.send_request(
            "textDocument/signatureHelp",
            {
                "textDocument": {"uri": uri},
                "position": {"line": line, "character": character},
            },
        )

        return result if result else None

    @property
    def is_running(self) -> bool:
        """Check if LSP server is running."""
        return self._process is not None and self._process.returncode is None

    @property
    def is_initialized(self) -> bool:
        """Check if LSP session is initialized."""
        return self._initialized
