"""Type stubs for urequests module (HTTP client)."""

from typing import Any, Dict, Iterator, Optional, Union


class Response:
    """HTTP response object.

    Example:
        import urequests

        r = urequests.get("http://api.example.com/data")
        print(r.status_code)  # 200
        print(r.text)  # Response body as string
        data = r.json()  # Parse JSON response
        r.close()
    """

    status_code: int
    """HTTP status code (e.g., 200, 404, 500)."""

    reason: str
    """HTTP status reason phrase (e.g., 'OK', 'Not Found')."""

    headers: Dict[str, str]
    """Response headers dictionary."""

    encoding: str
    """Response encoding (default: 'utf-8')."""

    @property
    def text(self) -> str:
        """Response body as decoded string."""
        ...

    @property
    def content(self) -> bytes:
        """Response body as bytes."""
        ...

    def json(self) -> Any:
        """Parse response body as JSON.

        Returns:
            Parsed JSON data (dict, list, etc.)

        Raises:
            ValueError: If response is not valid JSON
        """
        ...

    def close(self) -> None:
        """Close the response and release resources.

        Always call this when done with the response.
        """
        ...

    def __enter__(self) -> "Response":
        ...

    def __exit__(self, *args: Any) -> None:
        ...


def request(
    method: str,
    url: str,
    data: Optional[Union[bytes, str, Dict[str, Any]]] = None,
    json: Optional[Any] = None,
    headers: Optional[Dict[str, str]] = None,
    auth: Optional[tuple] = None,
    timeout: Optional[float] = None,
    parse_headers: bool = True,
    stream: bool = False
) -> Response:
    """Make an HTTP request.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        url: Request URL
        data: Request body (bytes, string, or form dict)
        json: JSON data to send (sets Content-Type automatically)
        headers: Additional request headers
        auth: (username, password) tuple for basic auth
        timeout: Request timeout in seconds
        parse_headers: Parse response headers
        stream: Stream response body

    Returns:
        Response object
    """
    ...


def get(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    auth: Optional[tuple] = None,
    timeout: Optional[float] = None,
    **kwargs: Any
) -> Response:
    """Make GET request.

    Args:
        url: Request URL
        headers: Request headers
        auth: Basic auth credentials
        timeout: Request timeout

    Returns:
        Response object
    """
    ...


def post(
    url: str,
    data: Optional[Union[bytes, str, Dict[str, Any]]] = None,
    json: Optional[Any] = None,
    headers: Optional[Dict[str, str]] = None,
    auth: Optional[tuple] = None,
    timeout: Optional[float] = None,
    **kwargs: Any
) -> Response:
    """Make POST request.

    Args:
        url: Request URL
        data: Request body
        json: JSON data to send
        headers: Request headers
        auth: Basic auth credentials
        timeout: Request timeout

    Returns:
        Response object
    """
    ...


def put(
    url: str,
    data: Optional[Union[bytes, str, Dict[str, Any]]] = None,
    json: Optional[Any] = None,
    headers: Optional[Dict[str, str]] = None,
    auth: Optional[tuple] = None,
    timeout: Optional[float] = None,
    **kwargs: Any
) -> Response:
    """Make PUT request."""
    ...


def patch(
    url: str,
    data: Optional[Union[bytes, str, Dict[str, Any]]] = None,
    json: Optional[Any] = None,
    headers: Optional[Dict[str, str]] = None,
    auth: Optional[tuple] = None,
    timeout: Optional[float] = None,
    **kwargs: Any
) -> Response:
    """Make PATCH request."""
    ...


def delete(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    auth: Optional[tuple] = None,
    timeout: Optional[float] = None,
    **kwargs: Any
) -> Response:
    """Make DELETE request."""
    ...


def head(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    auth: Optional[tuple] = None,
    timeout: Optional[float] = None,
    **kwargs: Any
) -> Response:
    """Make HEAD request (headers only, no body)."""
    ...
