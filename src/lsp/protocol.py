"""JSON-RPC protocol handling for LSP communication."""

import json
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class JSONRPCProtocol:
    """Handle LSP JSON-RPC message framing.

    LSP uses a Content-Length header followed by the JSON content.
    Format:
        Content-Length: <length>\r\n
        \r\n
        <JSON content>
    """

    @staticmethod
    def encode(message: dict[str, Any]) -> bytes:
        """Encode a message with Content-Length header.

        Args:
            message: Dictionary to encode as JSON

        Returns:
            Bytes with Content-Length header and JSON content
        """
        content = json.dumps(message).encode("utf-8")
        header = f"Content-Length: {len(content)}\r\n\r\n"
        return header.encode("ascii") + content

    @staticmethod
    async def decode(reader: Any) -> Optional[dict[str, Any]]:
        """Decode a message from a Content-Length framed stream.

        Args:
            reader: Async stream reader

        Returns:
            Decoded message dictionary or None on EOF
        """
        # Read headers
        headers: dict[str, str] = {}
        while True:
            line = await reader.readline()
            if not line:
                return None  # EOF

            line_str = line.decode("ascii").strip()
            if not line_str:
                break  # Empty line marks end of headers

            if ":" in line_str:
                key, value = line_str.split(":", 1)
                headers[key.strip().lower()] = value.strip()

        # Get content length
        content_length_str = headers.get("content-length")
        if not content_length_str:
            logger.warning("Missing Content-Length header")
            return None

        try:
            content_length = int(content_length_str)
        except ValueError:
            logger.warning("Invalid Content-Length: %s", content_length_str)
            return None

        # Read content
        content = await reader.readexactly(content_length)
        if not content:
            return None

        try:
            return json.loads(content.decode("utf-8"))
        except json.JSONDecodeError as e:
            logger.warning("Invalid JSON in LSP message: %s", e)
            return None

    @staticmethod
    def decode_sync(data: bytes) -> tuple[Optional[dict[str, Any]], bytes]:
        """Decode a message from bytes (synchronous version).

        Args:
            data: Bytes buffer containing message(s)

        Returns:
            Tuple of (decoded message or None, remaining bytes)
        """
        # Find header end
        header_end = data.find(b"\r\n\r\n")
        if header_end == -1:
            return None, data  # Incomplete header

        # Parse headers
        header_bytes = data[:header_end]
        headers: dict[str, str] = {}
        for line in header_bytes.decode("ascii").split("\r\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip().lower()] = value.strip()

        # Get content length
        content_length_str = headers.get("content-length")
        if not content_length_str:
            return None, data

        try:
            content_length = int(content_length_str)
        except ValueError:
            return None, data

        # Check if we have complete content
        content_start = header_end + 4
        content_end = content_start + content_length

        if len(data) < content_end:
            return None, data  # Incomplete content

        # Extract content
        content = data[content_start:content_end]
        remaining = data[content_end:]

        try:
            message = json.loads(content.decode("utf-8"))
            return message, remaining
        except json.JSONDecodeError:
            return None, remaining

    @staticmethod
    def create_request(
        request_id: int,
        method: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Create a JSON-RPC request.

        Args:
            request_id: Unique request ID
            method: LSP method name
            params: Method parameters

        Returns:
            Request dictionary
        """
        request: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
        }
        if params is not None:
            request["params"] = params
        return request

    @staticmethod
    def create_notification(
        method: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Create a JSON-RPC notification (no response expected).

        Args:
            method: LSP method name
            params: Method parameters

        Returns:
            Notification dictionary
        """
        notification: dict[str, Any] = {
            "jsonrpc": "2.0",
            "method": method,
        }
        if params is not None:
            notification["params"] = params
        return notification

    @staticmethod
    def create_response(
        request_id: int,
        result: Optional[Any] = None,
        error: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Create a JSON-RPC response.

        Args:
            request_id: Request ID being responded to
            result: Success result
            error: Error object (code, message, data)

        Returns:
            Response dictionary
        """
        response: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": request_id,
        }
        if error is not None:
            response["error"] = error
        else:
            response["result"] = result
        return response
