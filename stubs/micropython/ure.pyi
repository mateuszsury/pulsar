"""Type stubs for MicroPython ure module (regular expressions)."""

from typing import Any, Callable, Iterator, List, Optional, Tuple, Union

# Flags
DEBUG: int
IGNORECASE: int
MULTILINE: int
DOTALL: int
VERBOSE: int
ASCII: int


class Match:
    """Match object returned by match/search operations."""

    def group(self, index: int = 0) -> Optional[str]:
        """Return matched group.

        Args:
            index: Group number (0 = entire match)

        Returns:
            Matched string or None
        """
        ...

    def groups(self) -> Tuple[Optional[str], ...]:
        """Return all matched groups.

        Returns:
            Tuple of matched group strings
        """
        ...

    def start(self, index: int = 0) -> int:
        """Return start position of match.

        Args:
            index: Group number

        Returns:
            Start index in original string
        """
        ...

    def end(self, index: int = 0) -> int:
        """Return end position of match.

        Args:
            index: Group number

        Returns:
            End index in original string
        """
        ...

    def span(self, index: int = 0) -> Tuple[int, int]:
        """Return (start, end) positions of match.

        Args:
            index: Group number

        Returns:
            Tuple of (start, end) indices
        """
        ...


class Pattern:
    """Compiled regular expression pattern."""

    def match(self, string: str, pos: int = 0, endpos: int = -1) -> Optional[Match]:
        """Match pattern at start of string.

        Args:
            string: String to match against
            pos: Start position
            endpos: End position (-1 = end of string)

        Returns:
            Match object or None
        """
        ...

    def search(self, string: str, pos: int = 0, endpos: int = -1) -> Optional[Match]:
        """Search for pattern anywhere in string.

        Args:
            string: String to search
            pos: Start position
            endpos: End position

        Returns:
            Match object or None
        """
        ...

    def sub(
        self,
        repl: Union[str, Callable[[Match], str]],
        string: str,
        count: int = 0
    ) -> str:
        """Replace pattern matches.

        Args:
            repl: Replacement string or function
            string: String to process
            count: Max replacements (0 = all)

        Returns:
            Modified string
        """
        ...

    def split(self, string: str, maxsplit: int = 0) -> List[str]:
        """Split string by pattern.

        Args:
            string: String to split
            maxsplit: Max splits (0 = unlimited)

        Returns:
            List of substrings
        """
        ...

    def findall(self, string: str) -> List[str]:
        """Find all matches.

        Args:
            string: String to search

        Returns:
            List of matching strings
        """
        ...


def compile(pattern: str, flags: int = 0) -> Pattern:
    """Compile a regular expression pattern.

    Args:
        pattern: Regex pattern string
        flags: Compilation flags (DEBUG, IGNORECASE, etc.)

    Returns:
        Compiled Pattern object
    """
    ...


def match(pattern: str, string: str, flags: int = 0) -> Optional[Match]:
    """Match pattern at start of string.

    Args:
        pattern: Regex pattern
        string: String to match
        flags: Match flags

    Returns:
        Match object or None
    """
    ...


def search(pattern: str, string: str, flags: int = 0) -> Optional[Match]:
    """Search for pattern in string.

    Args:
        pattern: Regex pattern
        string: String to search
        flags: Match flags

    Returns:
        Match object or None
    """
    ...


def sub(
    pattern: str,
    repl: Union[str, Callable[[Match], str]],
    string: str,
    count: int = 0,
    flags: int = 0
) -> str:
    """Replace pattern matches in string.

    Args:
        pattern: Regex pattern
        repl: Replacement string or function
        string: String to process
        count: Max replacements (0 = all)
        flags: Match flags

    Returns:
        Modified string
    """
    ...


def split(pattern: str, string: str, maxsplit: int = 0, flags: int = 0) -> List[str]:
    """Split string by pattern.

    Args:
        pattern: Regex pattern
        string: String to split
        maxsplit: Max splits
        flags: Match flags

    Returns:
        List of substrings
    """
    ...


def findall(pattern: str, string: str, flags: int = 0) -> List[str]:
    """Find all matches in string.

    Args:
        pattern: Regex pattern
        string: String to search
        flags: Match flags

    Returns:
        List of matching strings
    """
    ...


def escape(string: str) -> str:
    """Escape special regex characters.

    Args:
        string: String with special characters

    Returns:
        Escaped string safe for regex
    """
    ...
