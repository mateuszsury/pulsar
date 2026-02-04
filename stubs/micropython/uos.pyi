"""Type stubs for MicroPython uos module (OS functions)."""

from typing import Any, Iterator, Optional, Tuple, Union

# VFS flags
VFS_MOUNT_RO: int

def uname() -> Tuple[str, str, str, str, str]:
    """Get system/OS information.

    Returns:
        Tuple of (sysname, nodename, release, version, machine)
    """
    ...

def urandom(n: int) -> bytes:
    """Generate n random bytes.

    Args:
        n: Number of bytes to generate

    Returns:
        Random bytes
    """
    ...

def chdir(path: str) -> None:
    """Change current directory.

    Args:
        path: Directory path
    """
    ...

def getcwd() -> str:
    """Get current working directory.

    Returns:
        Current directory path
    """
    ...

def listdir(dir: str = ".") -> list[str]:
    """List directory contents.

    Args:
        dir: Directory path (default: current directory)

    Returns:
        List of file/directory names
    """
    ...

def ilistdir(dir: str = ".") -> Iterator[Tuple[str, int, int, int]]:
    """Iterate over directory contents.

    Args:
        dir: Directory path

    Yields:
        Tuples of (name, type, inode, size)
        type: 0x4000 = directory, 0x8000 = regular file
    """
    ...

def mkdir(path: str) -> None:
    """Create a directory.

    Args:
        path: Directory path to create
    """
    ...

def rmdir(path: str) -> None:
    """Remove an empty directory.

    Args:
        path: Directory path to remove
    """
    ...

def remove(path: str) -> None:
    """Remove a file.

    Args:
        path: File path to remove
    """
    ...

def rename(old_path: str, new_path: str) -> None:
    """Rename a file or directory.

    Args:
        old_path: Current path
        new_path: New path
    """
    ...

def stat(path: str) -> Tuple[int, int, int, int, int, int, int, int, int, int]:
    """Get file/directory status.

    Args:
        path: File or directory path

    Returns:
        Tuple of (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)
    """
    ...

def statvfs(path: str) -> Tuple[int, int, int, int, int, int, int, int, int, int]:
    """Get filesystem statistics.

    Args:
        path: Path on the filesystem

    Returns:
        Tuple of (bsize, frsize, blocks, bfree, bavail, files, ffree, favail, flag, namemax)
    """
    ...

def sync() -> None:
    """Sync all filesystems."""
    ...

def dupterm(
    stream: Optional[Any],
    index: int = 0
) -> Optional[Any]:
    """Duplicate terminal on a stream.

    Args:
        stream: Stream object (None to remove)
        index: Slot index (0 or 1)

    Returns:
        Previous stream or None
    """
    ...

def mount(
    fsobj: Any,
    path: str,
    *,
    readonly: bool = False
) -> None:
    """Mount a filesystem.

    Args:
        fsobj: Filesystem object
        path: Mount point
        readonly: Mount as read-only
    """
    ...

def umount(path: str) -> None:
    """Unmount a filesystem.

    Args:
        path: Mount point
    """
    ...


class VfsFat:
    """FAT filesystem for SD cards."""

    def __init__(self, block_dev: Any) -> None:
        """Create FAT filesystem on block device.

        Args:
            block_dev: Block device with readblocks/writeblocks
        """
        ...

    @staticmethod
    def mkfs(block_dev: Any) -> None:
        """Create FAT filesystem on block device."""
        ...


class VfsLfs1:
    """LittleFS v1 filesystem."""

    def __init__(
        self,
        block_dev: Any,
        readsize: int = 32,
        progsize: int = 32,
        lookahead: int = 32
    ) -> None:
        """Create LittleFS v1 filesystem.

        Args:
            block_dev: Block device
            readsize: Read block size
            progsize: Program block size
            lookahead: Lookahead size
        """
        ...

    @staticmethod
    def mkfs(block_dev: Any, **kwargs: Any) -> None:
        """Create LittleFS v1 filesystem on block device."""
        ...


class VfsLfs2:
    """LittleFS v2 filesystem."""

    def __init__(
        self,
        block_dev: Any,
        readsize: int = 32,
        progsize: int = 32,
        lookahead: int = 32,
        mtime: bool = True
    ) -> None:
        """Create LittleFS v2 filesystem.

        Args:
            block_dev: Block device
            readsize: Read block size
            progsize: Program block size
            lookahead: Lookahead size
            mtime: Store modification times
        """
        ...

    @staticmethod
    def mkfs(block_dev: Any, **kwargs: Any) -> None:
        """Create LittleFS v2 filesystem on block device."""
        ...
