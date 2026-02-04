"""Type stubs for MicroPython uselect module (I/O multiplexing)."""

from typing import Any, List, Optional, Tuple

# Event flags
POLLIN: int    # Data available to read
POLLOUT: int   # Ready for writing
POLLERR: int   # Error condition
POLLHUP: int   # Hang up


class poll:
    """Poll object for monitoring multiple I/O streams.

    Example:
        import uselect
        import usocket

        sock = usocket.socket()
        # ... connect socket ...

        poller = uselect.poll()
        poller.register(sock, uselect.POLLIN)

        events = poller.poll(1000)  # Wait up to 1 second
        for obj, event in events:
            if event & uselect.POLLIN:
                data = obj.read()
    """

    def register(self, obj: Any, eventmask: int = POLLIN | POLLOUT) -> None:
        """Register object for polling.

        Args:
            obj: Stream object (socket, file, etc.)
            eventmask: Events to monitor (POLLIN, POLLOUT, etc.)
        """
        ...

    def unregister(self, obj: Any) -> None:
        """Remove object from polling.

        Args:
            obj: Previously registered object
        """
        ...

    def modify(self, obj: Any, eventmask: int) -> None:
        """Modify event mask for registered object.

        Args:
            obj: Registered object
            eventmask: New event mask
        """
        ...

    def poll(self, timeout: int = -1) -> List[Tuple[Any, int]]:
        """Wait for events.

        Args:
            timeout: Timeout in milliseconds (-1 = wait forever, 0 = return immediately)

        Returns:
            List of (object, event) tuples for objects with events
        """
        ...

    def ipoll(self, timeout: int = -1, flags: int = 0) -> Any:
        """Iterate over events (memory-efficient).

        Args:
            timeout: Timeout in milliseconds
            flags: Additional flags

        Yields:
            (object, event) tuples

        Note:
            Unlike poll(), ipoll() reuses same tuple for all results.
            Process each result before getting next.
        """
        ...


def select(
    rlist: List[Any],
    wlist: List[Any],
    xlist: List[Any],
    timeout: Optional[float] = None
) -> Tuple[List[Any], List[Any], List[Any]]:
    """Wait for I/O events (Unix select-style).

    Args:
        rlist: Objects to check for reading
        wlist: Objects to check for writing
        xlist: Objects to check for exceptions
        timeout: Timeout in seconds (None = wait forever)

    Returns:
        Tuple of (readable, writable, exceptional) lists
    """
    ...
