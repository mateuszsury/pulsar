"""Folder synchronization between PC and MicroPython device."""

import asyncio
import hashlib
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from serial_comm.manager import SerialManager

logger = logging.getLogger(__name__)


@dataclass
class SyncFile:
    """Represents a file for synchronization."""

    path: str  # Relative path
    local_path: Path | None  # Full local path
    size: int
    local_hash: str | None = None
    remote_hash: str | None = None

    @property
    def needs_upload(self) -> bool:
        """Check if file needs to be uploaded."""
        if self.local_hash is None:
            return False
        if self.remote_hash is None:
            return True
        return self.local_hash != self.remote_hash

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "size": self.size,
            "local_hash": self.local_hash,
            "remote_hash": self.remote_hash,
            "needs_upload": self.needs_upload,
        }


@dataclass
class SyncResult:
    """Result of a sync operation."""

    uploaded: list[str]
    failed: list[str]
    skipped: list[str]
    errors: list[str]

    def to_dict(self) -> dict:
        return {
            "uploaded": self.uploaded,
            "failed": self.failed,
            "skipped": self.skipped,
            "errors": self.errors,
            "success": len(self.failed) == 0 and len(self.errors) == 0,
        }


class FolderSync:
    """Handles folder synchronization with MicroPython devices."""

    # Files/folders to ignore during sync
    IGNORE_PATTERNS = {
        "__pycache__",
        ".git",
        ".vscode",
        ".idea",
        "*.pyc",
        "*.pyo",
        ".DS_Store",
        "Thumbs.db",
        ".env",
    }

    def __init__(
        self,
        serial_manager: "SerialManager",
        on_progress: Callable[[str, float, str], None] | None = None,
    ) -> None:
        self.serial_manager = serial_manager
        self._on_progress = on_progress

    def _should_ignore(self, path: Path) -> bool:
        """Check if a file/folder should be ignored."""
        name = path.name

        for pattern in self.IGNORE_PATTERNS:
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern:
                return True

        return False

    def _file_hash(self, path: Path) -> str:
        """Calculate MD5 hash of a file."""
        hasher = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    async def _get_remote_files(self, port: str, remote_path: str = "/") -> dict[str, int]:
        """Get list of files on device with sizes."""
        files = await self.serial_manager.list_files(port, remote_path)
        result = {}

        for f in files:
            if f.get("type") == "file":
                result[f["name"]] = f.get("size", 0)
            elif f.get("type") == "directory":
                # Recursively get files in subdirectory
                subpath = f"{remote_path}/{f['name']}".replace("//", "/")
                subfiles = await self._get_remote_files(port, subpath)
                for name, size in subfiles.items():
                    result[f"{f['name']}/{name}"] = size

        return result

    async def _get_remote_hash(self, port: str, path: str) -> str | None:
        """Calculate hash of a remote file using MicroPython."""
        code = f'''
import hashlib
try:
    h = hashlib.md5()
    with open("{path}", "rb") as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            h.update(chunk)
    print(h.hexdigest())
except Exception as e:
    print("ERROR:" + str(e))
'''
        result = await self.serial_manager.execute(port, code, timeout=30)
        if result.success and result.output:
            output = result.output.strip()
            if output.startswith("ERROR:"):
                return None
            return output
        return None

    def scan_local_folder(self, folder: Path) -> list[SyncFile]:
        """Scan local folder for files to sync."""
        files = []

        for root, dirs, filenames in os.walk(folder):
            root_path = Path(root)

            # Filter ignored directories
            dirs[:] = [d for d in dirs if not self._should_ignore(root_path / d)]

            for filename in filenames:
                file_path = root_path / filename

                if self._should_ignore(file_path):
                    continue

                rel_path = file_path.relative_to(folder)

                files.append(SyncFile(
                    path=str(rel_path).replace("\\", "/"),
                    local_path=file_path,
                    size=file_path.stat().st_size,
                    local_hash=self._file_hash(file_path),
                ))

        return files

    async def compare_files(
        self,
        port: str,
        local_folder: Path,
        remote_folder: str = "/",
    ) -> list[SyncFile]:
        """Compare local and remote files."""
        # Get local files
        local_files = self.scan_local_folder(local_folder)

        # Get remote files
        remote_files = await self._get_remote_files(port, remote_folder)

        # Compare and get remote hashes for files that exist
        total = len(local_files)
        for i, file in enumerate(local_files):
            if self._on_progress:
                self._on_progress(file.path, (i + 1) / total, "Comparing")

            remote_path = f"{remote_folder}/{file.path}".replace("//", "/")

            if file.path in remote_files:
                # File exists remotely, check hash
                remote_size = remote_files[file.path]
                if remote_size != file.size:
                    # Different size, definitely needs upload
                    file.remote_hash = "different_size"
                else:
                    # Same size, check hash
                    file.remote_hash = await self._get_remote_hash(port, remote_path)
            else:
                # File doesn't exist remotely
                file.remote_hash = None

        return local_files

    async def sync_folder(
        self,
        port: str,
        local_folder: Path,
        remote_folder: str = "/",
        dry_run: bool = False,
    ) -> SyncResult:
        """Synchronize local folder with device."""
        result = SyncResult(
            uploaded=[],
            failed=[],
            skipped=[],
            errors=[],
        )

        try:
            # Compare files
            files = await self.compare_files(port, local_folder, remote_folder)

            # Upload files that need it
            total = len(files)
            for i, file in enumerate(files):
                if self._on_progress:
                    self._on_progress(file.path, (i + 1) / total, "Syncing")

                if not file.needs_upload:
                    result.skipped.append(file.path)
                    continue

                if dry_run:
                    result.uploaded.append(file.path)
                    continue

                try:
                    # Ensure remote directory exists
                    remote_path = f"{remote_folder}/{file.path}".replace("//", "/")
                    remote_dir = "/".join(remote_path.split("/")[:-1])
                    if remote_dir and remote_dir != "/":
                        await self._ensure_remote_dir(port, remote_dir)

                    # Read local file
                    with open(file.local_path, "rb") as f:
                        content = f.read()

                    # Upload
                    success = await self.serial_manager.write_file(port, remote_path, content)

                    if success:
                        result.uploaded.append(file.path)
                        logger.info("Uploaded: %s", file.path)
                    else:
                        result.failed.append(file.path)
                        logger.error("Failed to upload: %s", file.path)

                except Exception as e:
                    result.failed.append(file.path)
                    result.errors.append(f"{file.path}: {e}")
                    logger.exception("Error uploading %s: %s", file.path, e)

        except Exception as e:
            result.errors.append(str(e))
            logger.exception("Sync error: %s", e)

        return result

    async def _ensure_remote_dir(self, port: str, path: str) -> None:
        """Ensure a directory exists on the device."""
        parts = path.strip("/").split("/")
        current = ""

        for part in parts:
            current = f"{current}/{part}"
            try:
                await self.serial_manager.mkdir(port, current)
            except Exception:
                pass  # Directory might already exist
