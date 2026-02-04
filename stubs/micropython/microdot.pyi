"""Type stubs for microdot module (async web framework)."""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union


class Request:
    """HTTP request object."""

    app: "Microdot"
    """The application instance."""

    method: str
    """HTTP method (GET, POST, etc.)."""

    path: str
    """Request path."""

    query_string: str
    """Query string (without leading ?)."""

    args: Dict[str, str]
    """Parsed query parameters."""

    headers: Dict[str, str]
    """Request headers."""

    cookies: Dict[str, str]
    """Request cookies."""

    content_length: int
    """Content-Length header value."""

    content_type: str
    """Content-Type header value."""

    body: bytes
    """Raw request body."""

    client_addr: Tuple[str, int]
    """Client (ip, port) tuple."""

    @property
    def json(self) -> Any:
        """Parse request body as JSON."""
        ...

    @property
    def form(self) -> Dict[str, str]:
        """Parse form data from request body."""
        ...

    def url_for(self, endpoint: str, **kwargs: Any) -> str:
        """Generate URL for an endpoint.

        Args:
            endpoint: Route function name
            kwargs: URL parameters
        """
        ...


class Response:
    """HTTP response object."""

    status_code: int
    """HTTP status code."""

    headers: Dict[str, str]
    """Response headers."""

    body: Union[str, bytes]
    """Response body."""

    def __init__(
        self,
        body: Union[str, bytes, Any] = "",
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        content_type: Optional[str] = None
    ) -> None:
        """Create response.

        Args:
            body: Response body
            status_code: HTTP status code
            headers: Response headers
            content_type: Content-Type header
        """
        ...

    def set_cookie(
        self,
        name: str,
        value: str,
        path: str = "/",
        domain: Optional[str] = None,
        expires: Optional[str] = None,
        max_age: Optional[int] = None,
        secure: bool = False,
        http_only: bool = False
    ) -> None:
        """Set a cookie.

        Args:
            name: Cookie name
            value: Cookie value
            path: Cookie path
            domain: Cookie domain
            expires: Expiration date string
            max_age: Max age in seconds
            secure: Secure flag
            http_only: HttpOnly flag
        """
        ...

    def delete_cookie(self, name: str, path: str = "/") -> None:
        """Delete a cookie."""
        ...

    @staticmethod
    def redirect(url: str, status_code: int = 302) -> "Response":
        """Create redirect response.

        Args:
            url: Redirect URL
            status_code: 301 (permanent) or 302 (temporary)
        """
        ...

    @staticmethod
    def send_file(
        path: str,
        content_type: Optional[str] = None,
        max_age: int = 0
    ) -> "Response":
        """Create response to send a file.

        Args:
            path: File path
            content_type: MIME type (auto-detected if None)
            max_age: Cache max-age in seconds
        """
        ...


def jsonify(data: Any, status_code: int = 200) -> Response:
    """Create JSON response.

    Args:
        data: Data to serialize as JSON
        status_code: HTTP status code

    Returns:
        Response with JSON content-type
    """
    ...


class Microdot:
    """Async web framework for MicroPython.

    Example:
        from microdot import Microdot

        app = Microdot()

        @app.route('/')
        async def index(request):
            return 'Hello World'

        @app.route('/user/<name>')
        async def user(request, name):
            return f'Hello {name}'

        app.run(port=8080)
    """

    def __init__(self) -> None:
        """Create Microdot application."""
        ...

    def route(
        self,
        path: str,
        methods: Optional[List[str]] = None
    ) -> Callable:
        """Register a route handler.

        Args:
            path: URL path (can include <param> placeholders)
            methods: Allowed HTTP methods (default: ['GET'])

        Returns:
            Decorator function
        """
        ...

    def get(self, path: str) -> Callable:
        """Register GET route handler."""
        ...

    def post(self, path: str) -> Callable:
        """Register POST route handler."""
        ...

    def put(self, path: str) -> Callable:
        """Register PUT route handler."""
        ...

    def patch(self, path: str) -> Callable:
        """Register PATCH route handler."""
        ...

    def delete(self, path: str) -> Callable:
        """Register DELETE route handler."""
        ...

    def before_request(self, f: Callable) -> Callable:
        """Register before request handler.

        Args:
            f: Function called before each request
        """
        ...

    def after_request(self, f: Callable) -> Callable:
        """Register after request handler.

        Args:
            f: Function called after each request
        """
        ...

    def errorhandler(self, status_code_or_exception: Union[int, type]) -> Callable:
        """Register error handler.

        Args:
            status_code_or_exception: HTTP status code or exception class
        """
        ...

    def mount(self, prefix: str, app: "Microdot") -> None:
        """Mount another Microdot app at a URL prefix.

        Args:
            prefix: URL prefix
            app: Microdot application to mount
        """
        ...

    def run(
        self,
        host: str = "0.0.0.0",
        port: int = 5000,
        debug: bool = False,
        ssl: Any = None
    ) -> None:
        """Run the application (blocking).

        Args:
            host: Bind address
            port: Port number
            debug: Enable debug mode
            ssl: SSL context
        """
        ...

    async def start_server(
        self,
        host: str = "0.0.0.0",
        port: int = 5000,
        debug: bool = False,
        ssl: Any = None
    ) -> Any:
        """Start server as async task.

        Args:
            host: Bind address
            port: Port number
            debug: Enable debug mode
            ssl: SSL context

        Returns:
            Server object
        """
        ...

    def shutdown(self) -> None:
        """Shutdown the server."""
        ...
