"""Raw REPL protocol implementation."""

import asyncio
import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .device import Device

logger = logging.getLogger(__name__)


# Raw REPL control characters
CTRL_A = b"\x01"  # Enter raw REPL
CTRL_B = b"\x02"  # Exit raw REPL
CTRL_C = b"\x03"  # Interrupt
CTRL_D = b"\x04"  # Soft reset / Execute in raw REPL
CTRL_E = b"\x05"  # Paste mode

# Raw REPL responses
RAW_REPL_PROMPT = b">"
RAW_REPL_OK = b"OK"


@dataclass
class REPLResult:
    """Result of REPL code execution."""

    output: str
    error: str
    success: bool

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "output": self.output,
            "error": self.error,
            "success": self.success,
        }


class RawREPL:
    """Raw REPL protocol for reliable code execution."""

    def __init__(self, device: "Device") -> None:
        self.device = device
        self._in_raw_mode = False
        self._lock = asyncio.Lock()

    async def enter_raw_mode(self) -> bool:
        """Enter raw REPL mode."""
        if self._in_raw_mode:
            return True

        await self.device.pause_read_loop()
        try:
            # Send Ctrl+C to interrupt any running code
            await self.device.write(CTRL_C)
            await asyncio.sleep(0.1)

            # Clear buffer
            await self.device.read(timeout=0.2)

            # Enter raw REPL with Ctrl+A
            await self.device.write(CTRL_A)
            await asyncio.sleep(0.1)

            # Check for raw REPL prompt
            response = await self.device.read(timeout=1.0)
            if b"raw REPL" in response or b">" in response:
                self._in_raw_mode = True
                logger.debug("Entered raw REPL mode")
                return True

            logger.warning("Failed to enter raw REPL: %s", response)
            return False

        except Exception as e:
            logger.exception("Error entering raw REPL: %s", e)
            return False
        finally:
            self.device.resume_read_loop()

    async def exit_raw_mode(self) -> None:
        """Exit raw REPL mode."""
        if not self._in_raw_mode:
            return

        try:
            await self.device.write(CTRL_B)
            await asyncio.sleep(0.1)
            self._in_raw_mode = False
            logger.debug("Exited raw REPL mode")
        except Exception as e:
            logger.exception("Error exiting raw REPL: %s", e)

    async def execute(
        self,
        code: str,
        timeout: float = 30.0,
    ) -> REPLResult:
        """
        Execute Python code in raw REPL mode.

        Args:
            code: Python code to execute.
            timeout: Execution timeout in seconds.

        Returns:
            REPLResult with output and error.
        """
        async with self._lock:
            # Enter raw REPL if needed
            if not self._in_raw_mode:
                if not await self.enter_raw_mode():
                    return REPLResult(
                        output="",
                        error="Failed to enter raw REPL mode",
                        success=False,
                    )

            await self.device.pause_read_loop()
            try:
                # Clear any pending data
                await self.device.read(timeout=0.1)

                # Send code
                code_bytes = code.encode("utf-8")
                await self.device.write(code_bytes)

                # Execute with Ctrl+D
                await self.device.write(CTRL_D)

                # Wait for OK
                response = await self.device.read_until(b"OK", timeout=2.0)
                if b"OK" not in response:
                    return REPLResult(
                        output="",
                        error="No OK response from device",
                        success=False,
                    )

                # Read output until EOT (Ctrl+D)
                output_bytes = b""
                error_bytes = b""

                try:
                    # Read until we get the raw REPL prompt back
                    data = await asyncio.wait_for(
                        self._read_raw_response(),
                        timeout=timeout,
                    )
                    output_bytes, error_bytes = data
                except asyncio.TimeoutError:
                    return REPLResult(
                        output="",
                        error="Execution timeout",
                        success=False,
                    )

                output = output_bytes.decode("utf-8", errors="replace")
                error = error_bytes.decode("utf-8", errors="replace")

                return REPLResult(
                    output=output,
                    error=error,
                    success=not bool(error),
                )

            except Exception as e:
                logger.exception("Execution error: %s", e)
                return REPLResult(
                    output="",
                    error=str(e),
                    success=False,
                )
            finally:
                self.device.resume_read_loop()

    async def _read_raw_response(self) -> tuple[bytes, bytes]:
        """Read raw REPL response (output and error)."""
        output = b""
        error = b""

        # Raw REPL format: OK<output>\x04<error>\x04>
        # First \x04 separates output from error
        # Second \x04 marks end, followed by >

        data = b""
        while True:
            chunk = await self.device.read(1024, timeout=0.5)
            if not chunk:
                continue
            data += chunk

            # Check for end marker
            if data.endswith(b"\x04>"):
                break

        # Parse output and error
        parts = data.split(b"\x04")
        if len(parts) >= 2:
            output = parts[0]
            error = parts[1].rstrip(b">")

        return output, error

    async def execute_friendly(self, code: str) -> REPLResult:
        """
        Execute code in friendly REPL mode (normal mode).

        This is slower but shows output as it happens.
        """
        async with self._lock:
            # Exit raw mode if in it
            if self._in_raw_mode:
                await self.exit_raw_mode()

            await self.device.pause_read_loop()
            try:
                # Clear buffer
                await self.device.read(timeout=0.1)

                # Send code line by line
                lines = code.strip().split("\n")
                for line in lines:
                    await self.device.write_line(line)
                    await asyncio.sleep(0.05)

                # Wait for execution
                await asyncio.sleep(0.5)

                # Read all output
                output = await self.device.read(timeout=2.0)
                text = output.decode("utf-8", errors="replace")

                # Check for errors
                error = ""
                if "Traceback" in text or "Error" in text:
                    error = text
                    text = ""

                return REPLResult(
                    output=text,
                    error=error,
                    success=not bool(error),
                )

            except Exception as e:
                return REPLResult(
                    output="",
                    error=str(e),
                    success=False,
                )
            finally:
                self.device.resume_read_loop()

    async def soft_reset(self) -> bool:
        """Perform soft reset."""
        await self.device.pause_read_loop()
        try:
            # Exit raw mode first
            if self._in_raw_mode:
                await self.exit_raw_mode()

            # Send Ctrl+D for soft reset
            await self.device.write(CTRL_D)
            await asyncio.sleep(1.0)

            # Wait for boot message
            response = await self.device.read(timeout=3.0)
            return b"MicroPython" in response or b">>>" in response

        except Exception as e:
            logger.exception("Soft reset error: %s", e)
            return False
        finally:
            self.device.resume_read_loop()
