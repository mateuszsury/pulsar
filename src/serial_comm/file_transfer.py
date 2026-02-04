"""File transfer operations for MicroPython devices."""

import asyncio
import base64
import logging
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .repl import RawREPL

logger = logging.getLogger(__name__)

# Chunk size for file transfer (base64 adds ~33% overhead)
CHUNK_SIZE = 512


@dataclass
class FileInfo:
    """Information about a file on the device."""

    name: str
    path: str
    is_dir: bool
    size: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "path": self.path,
            "is_dir": self.is_dir,
            "size": self.size,
        }


class FileTransfer:
    """File transfer operations using raw REPL."""

    def __init__(
        self,
        repl: "RawREPL",
        on_progress: Callable[[str, float], None] | None = None,
    ) -> None:
        self.repl = repl
        self._on_progress = on_progress

    async def list_files(self, path: str = "/") -> list[FileInfo]:
        """List files in a directory."""
        code = f"""
import os
try:
    for name in os.listdir({repr(path)}):
        full_path = {repr(path)} + '/' + name if {repr(path)} != '/' else '/' + name
        try:
            stat = os.stat(full_path)
            is_dir = stat[0] & 0x4000
            size = stat[6] if not is_dir else 0
            print(repr((name, full_path, bool(is_dir), size)))
        except:
            print(repr((name, full_path, False, 0)))
except Exception as e:
    print('ERROR:', e)
"""
        result = await self.repl.execute(code)

        files = []
        for line in result.output.strip().split("\n"):
            line = line.strip()
            if line and line.startswith("("):
                try:
                    data = eval(line)  # Safe: we control the output format
                    files.append(FileInfo(
                        name=data[0],
                        path=data[1],
                        is_dir=data[2],
                        size=data[3],
                    ))
                except Exception as e:
                    logger.warning("Failed to parse file info: %s", e)

        return files

    async def read_file(self, path: str) -> bytes:
        """Read a file from the device."""
        # First get file size
        code = f"""
import os
try:
    stat = os.stat({repr(path)})
    print(stat[6])
except Exception as e:
    print('ERROR:', e)
"""
        result = await self.repl.execute(code)

        try:
            file_size = int(result.output.strip())
        except ValueError:
            raise FileNotFoundError(f"File not found: {path}")

        # Read file in chunks using base64
        content = b""
        offset = 0

        while offset < file_size:
            chunk_size = min(CHUNK_SIZE, file_size - offset)
            code = f"""
import ubinascii
with open({repr(path)}, 'rb') as f:
    f.seek({offset})
    data = f.read({chunk_size})
    print(ubinascii.b2a_base64(data).decode().strip())
"""
            result = await self.repl.execute(code)

            if result.error:
                raise IOError(f"Read error: {result.error}")

            chunk = base64.b64decode(result.output.strip())
            content += chunk
            offset += len(chunk)

            if self._on_progress:
                self._on_progress(path, offset / file_size)

        return content

    async def write_file(
        self,
        path: str,
        content: bytes,
        mkdir: bool = True,
    ) -> bool:
        """Write a file to the device."""
        # Create parent directory if needed
        if mkdir:
            parent = str(PurePosixPath(path).parent)
            if parent and parent != "/":
                await self.mkdir(parent)

        # Write file in chunks using base64
        total_size = len(content)
        offset = 0

        # Open file for writing
        code = f"f = open({repr(path)}, 'wb')"
        result = await self.repl.execute(code)
        if result.error:
            raise IOError(f"Failed to open file: {result.error}")

        try:
            while offset < total_size:
                chunk_size = min(CHUNK_SIZE, total_size - offset)
                chunk = content[offset:offset + chunk_size]
                b64_chunk = base64.b64encode(chunk).decode()

                code = f"""
import ubinascii
f.write(ubinascii.a2b_base64({repr(b64_chunk)}))
"""
                result = await self.repl.execute(code)

                if result.error:
                    raise IOError(f"Write error: {result.error}")

                offset += chunk_size

                if self._on_progress:
                    self._on_progress(path, offset / total_size)

            # Close file
            code = "f.close()"
            await self.repl.execute(code)

            return True

        except Exception:
            # Try to close file on error
            try:
                await self.repl.execute("f.close()")
            except Exception:
                pass
            raise

    async def delete_file(self, path: str) -> bool:
        """Delete a file from the device."""
        code = f"""
import os
try:
    os.remove({repr(path)})
    print('OK')
except Exception as e:
    print('ERROR:', e)
"""
        result = await self.repl.execute(code)
        return "OK" in result.output

    async def delete_dir(self, path: str, recursive: bool = False) -> bool:
        """Delete a directory from the device."""
        if recursive:
            # Recursively delete contents first
            files = await self.list_files(path)
            for file in files:
                if file.is_dir:
                    await self.delete_dir(file.path, recursive=True)
                else:
                    await self.delete_file(file.path)

        code = f"""
import os
try:
    os.rmdir({repr(path)})
    print('OK')
except Exception as e:
    print('ERROR:', e)
"""
        result = await self.repl.execute(code)
        return "OK" in result.output

    async def mkdir(self, path: str) -> bool:
        """Create a directory on the device."""
        # Create parent directories recursively
        parts = PurePosixPath(path).parts
        current = ""

        for part in parts:
            if not part or part == "/":
                current = "/"
                continue

            current = current + "/" + part if current != "/" else "/" + part

            code = f"""
import os
try:
    os.mkdir({repr(current)})
    print('OK')
except OSError as e:
    if e.args[0] == 17:  # EEXIST
        print('EXISTS')
    else:
        print('ERROR:', e)
"""
            result = await self.repl.execute(code)

            if "ERROR" in result.output:
                return False

        return True

    async def exists(self, path: str) -> bool:
        """Check if a file or directory exists."""
        code = f"""
import os
try:
    os.stat({repr(path)})
    print('YES')
except:
    print('NO')
"""
        result = await self.repl.execute(code)
        return "YES" in result.output

    async def get_size(self, path: str) -> int:
        """Get file size."""
        code = f"""
import os
try:
    stat = os.stat({repr(path)})
    print(stat[6])
except Exception as e:
    print('ERROR:', e)
"""
        result = await self.repl.execute(code)

        try:
            return int(result.output.strip())
        except ValueError:
            return -1
