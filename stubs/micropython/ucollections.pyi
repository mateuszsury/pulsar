"""Type stubs for MicroPython ucollections module."""

from typing import Any, Callable, Dict, Iterator, Optional, Tuple, Type, TypeVar

T = TypeVar('T')


class deque:
    """Double-ended queue with fixed maximum length.

    Example:
        from ucollections import deque

        d = deque((), 10)  # Max 10 items
        d.append(1)
        d.append(2)
        d.appendleft(0)
        print(d.popleft())  # 0
    """

    def __init__(self, iterable: tuple = (), maxlen: int = ...) -> None:
        """Create a deque.

        Args:
            iterable: Initial items
            maxlen: Maximum length (required in MicroPython)
        """
        ...

    def append(self, x: Any) -> None:
        """Add item to right end."""
        ...

    def appendleft(self, x: Any) -> None:
        """Add item to left end."""
        ...

    def pop(self) -> Any:
        """Remove and return item from right end."""
        ...

    def popleft(self) -> Any:
        """Remove and return item from left end."""
        ...

    def __len__(self) -> int:
        """Return number of items."""
        ...

    def __bool__(self) -> bool:
        """Return True if not empty."""
        ...


class OrderedDict(Dict[Any, Any]):
    """Dictionary that remembers insertion order.

    Example:
        from ucollections import OrderedDict

        od = OrderedDict()
        od['first'] = 1
        od['second'] = 2
        for key in od:
            print(key)  # first, second
    """

    def __init__(self, items: Any = None) -> None:
        """Create ordered dict.

        Args:
            items: Initial items (dict, list of tuples, etc.)
        """
        ...

    def clear(self) -> None:
        """Remove all items."""
        ...

    def copy(self) -> "OrderedDict":
        """Return shallow copy."""
        ...

    def get(self, key: Any, default: Any = None) -> Any:
        """Get item with default."""
        ...

    def items(self) -> Iterator[Tuple[Any, Any]]:
        """Return items iterator."""
        ...

    def keys(self) -> Iterator[Any]:
        """Return keys iterator."""
        ...

    def values(self) -> Iterator[Any]:
        """Return values iterator."""
        ...

    def pop(self, key: Any, default: Any = ...) -> Any:
        """Remove and return item."""
        ...

    def popitem(self, last: bool = True) -> Tuple[Any, Any]:
        """Remove and return last (or first) item.

        Args:
            last: Remove last item if True, first if False
        """
        ...

    def setdefault(self, key: Any, default: Any = None) -> Any:
        """Get item, setting default if missing."""
        ...

    def update(self, other: Any = None, **kwargs: Any) -> None:
        """Update from dict/iterable."""
        ...

    def move_to_end(self, key: Any, last: bool = True) -> None:
        """Move key to end (or beginning).

        Args:
            key: Key to move
            last: Move to end if True, beginning if False
        """
        ...


def namedtuple(
    name: str,
    fields: Tuple[str, ...],
    defaults: Optional[Tuple[Any, ...]] = None
) -> Type[Tuple[Any, ...]]:
    """Create a named tuple class.

    Args:
        name: Class name
        fields: Tuple of field names
        defaults: Default values for rightmost fields

    Returns:
        Named tuple class

    Example:
        Point = namedtuple('Point', ('x', 'y'))
        p = Point(10, 20)
        print(p.x, p.y)  # 10 20
    """
    ...
