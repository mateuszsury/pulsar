"""Type stubs for urandom module (pseudo-random numbers)."""

from typing import Optional, Sequence, TypeVar

T = TypeVar('T')


def seed(n: int = None) -> None:
    """Initialize random number generator.

    Args:
        n: Seed value (uses system time if None)
    """
    ...


def getrandbits(k: int) -> int:
    """Generate k random bits.

    Args:
        k: Number of bits

    Returns:
        Random integer with k bits
    """
    ...


def randrange(start: int, stop: int = None, step: int = 1) -> int:
    """Return random integer from range.

    Args:
        start: Start of range (or stop if only one arg)
        stop: End of range (exclusive)
        step: Step value

    Returns:
        Random integer from range(start, stop, step)

    Example:
        randrange(10)     # 0-9
        randrange(1, 7)   # 1-6
        randrange(0, 10, 2)  # 0, 2, 4, 6, or 8
    """
    ...


def randint(a: int, b: int) -> int:
    """Return random integer N such that a <= N <= b.

    Args:
        a: Lower bound (inclusive)
        b: Upper bound (inclusive)

    Returns:
        Random integer

    Example:
        randint(1, 6)  # Dice roll: 1-6
    """
    ...


def random() -> float:
    """Return random float in [0.0, 1.0).

    Returns:
        Random float from 0.0 to 1.0 (exclusive)
    """
    ...


def uniform(a: float, b: float) -> float:
    """Return random float N such that a <= N <= b.

    Args:
        a: Lower bound
        b: Upper bound

    Returns:
        Random float
    """
    ...


def choice(seq: Sequence[T]) -> T:
    """Return random element from sequence.

    Args:
        seq: Non-empty sequence

    Returns:
        Random element

    Example:
        choice(['red', 'green', 'blue'])
    """
    ...


def shuffle(seq: list) -> None:
    """Shuffle list in place.

    Args:
        seq: List to shuffle
    """
    ...
