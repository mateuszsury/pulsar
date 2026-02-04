"""Type stubs for MicroPython uasyncio module."""

from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Generator,
    Optional,
    TypeVar,
    Union,
    overload,
)

_T = TypeVar("_T")

class CancelledError(BaseException):
    """Exception raised when a task is cancelled."""
    ...

class TimeoutError(Exception):
    """Exception raised when an operation times out."""
    ...

class Task:
    """A scheduled coroutine."""

    def __init__(self, coro: Coroutine[Any, Any, _T]) -> None:
        ...

    def cancel(self) -> None:
        """Request cancellation of the task."""
        ...

    def done(self) -> bool:
        """Return True if the task has completed."""
        ...


class Event:
    """An event for task synchronization."""

    def __init__(self) -> None:
        """Create a new Event."""
        ...

    def set(self) -> None:
        """Set the event, waking all waiting tasks."""
        ...

    def clear(self) -> None:
        """Clear the event."""
        ...

    def is_set(self) -> bool:
        """Return True if the event is set."""
        ...

    async def wait(self) -> bool:
        """Wait until the event is set.

        Returns:
            True when the event is set
        """
        ...


class Lock:
    """A mutex lock for task synchronization."""

    def __init__(self) -> None:
        """Create a new Lock."""
        ...

    def locked(self) -> bool:
        """Return True if the lock is held."""
        ...

    async def acquire(self) -> bool:
        """Acquire the lock.

        Returns:
            True when the lock is acquired
        """
        ...

    def release(self) -> None:
        """Release the lock."""
        ...

    async def __aenter__(self) -> "Lock":
        ...

    async def __aexit__(self, *args: Any) -> None:
        ...


class ThreadSafeFlag:
    """A flag for signaling between threads/ISRs and asyncio."""

    def __init__(self) -> None:
        """Create a new ThreadSafeFlag."""
        ...

    def set(self) -> None:
        """Set the flag (can be called from ISR)."""
        ...

    def clear(self) -> None:
        """Clear the flag."""
        ...

    async def wait(self) -> None:
        """Wait until the flag is set."""
        ...


class StreamReader:
    """Async stream reader."""

    async def read(self, n: int = -1) -> bytes:
        """Read up to n bytes."""
        ...

    async def readline(self) -> bytes:
        """Read a line."""
        ...

    async def readexactly(self, n: int) -> bytes:
        """Read exactly n bytes."""
        ...


class StreamWriter:
    """Async stream writer."""

    def write(self, data: bytes) -> None:
        """Write data (may buffer)."""
        ...

    async def drain(self) -> None:
        """Wait until buffer is flushed."""
        ...

    def close(self) -> None:
        """Close the stream."""
        ...

    async def wait_closed(self) -> None:
        """Wait until the stream is closed."""
        ...

    def get_extra_info(self, name: str, default: Any = None) -> Any:
        """Get transport info."""
        ...


class Server:
    """Async TCP server."""

    async def wait_closed(self) -> None:
        """Wait until the server is closed."""
        ...

    def close(self) -> None:
        """Close the server."""
        ...


def create_task(coro: Coroutine[Any, Any, _T]) -> Task:
    """Schedule a coroutine to run.

    Args:
        coro: Coroutine to schedule

    Returns:
        Task object representing the scheduled coroutine
    """
    ...

def current_task() -> Task:
    """Return the currently running task."""
    ...

def run(coro: Coroutine[Any, Any, _T]) -> _T:
    """Run a coroutine until completion.

    Args:
        coro: Coroutine to run

    Returns:
        The return value of the coroutine
    """
    ...

async def sleep(t: float) -> None:
    """Sleep for t seconds.

    Args:
        t: Time in seconds (can be float)
    """
    ...

async def sleep_ms(t: int) -> None:
    """Sleep for t milliseconds.

    Args:
        t: Time in milliseconds
    """
    ...

@overload
async def wait_for(
    awaitable: Awaitable[_T],
    timeout: float
) -> _T:
    """Wait for an awaitable with timeout.

    Args:
        awaitable: The awaitable to wait for
        timeout: Timeout in seconds

    Returns:
        The result of the awaitable

    Raises:
        TimeoutError: If the timeout expires
    """
    ...

@overload
async def wait_for_ms(
    awaitable: Awaitable[_T],
    timeout: int
) -> _T:
    """Wait for an awaitable with timeout in milliseconds."""
    ...

async def gather(
    *awaitables: Awaitable[Any],
    return_exceptions: bool = False
) -> list[Any]:
    """Wait for multiple awaitables concurrently.

    Args:
        awaitables: Awaitables to run concurrently
        return_exceptions: If True, exceptions are returned as results

    Returns:
        List of results in the same order as awaitables
    """
    ...

async def open_connection(
    host: str,
    port: int,
    ssl: Any = None
) -> tuple[StreamReader, StreamWriter]:
    """Open a TCP connection.

    Args:
        host: Host to connect to
        port: Port number
        ssl: SSL context (optional)

    Returns:
        Tuple of (reader, writer)
    """
    ...

async def start_server(
    callback: Callable[[StreamReader, StreamWriter], Coroutine[Any, Any, None]],
    host: str,
    port: int,
    backlog: int = 5,
    ssl: Any = None
) -> Server:
    """Start a TCP server.

    Args:
        callback: Coroutine to handle each connection
        host: Host to bind to
        port: Port number
        backlog: Connection backlog
        ssl: SSL context (optional)

    Returns:
        Server object
    """
    ...

def new_event_loop() -> Any:
    """Create a new event loop."""
    ...

def get_event_loop() -> Any:
    """Get the current event loop."""
    ...

# For compatibility with CPython asyncio
class Loop:
    """Event loop (for compatibility)."""

    def run_forever(self) -> None:
        ...

    def run_until_complete(self, coro: Coroutine[Any, Any, _T]) -> _T:
        ...

    def stop(self) -> None:
        ...

    def close(self) -> None:
        ...

    def create_task(self, coro: Coroutine[Any, Any, _T]) -> Task:
        ...
