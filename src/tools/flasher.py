"""Firmware flasher and device info using esptool."""

import asyncio
import logging
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.events import EventBus

from core.events import EventType

logger = logging.getLogger(__name__)


@dataclass
class ChipInfo:
    """Information about ESP chip."""

    chip: str = ""
    chip_id: str = ""
    mac_address: str = ""
    flash_size: str = ""
    flash_type: str = ""
    crystal: str = ""
    features: list[str] = field(default_factory=list)
    raw_output: str = ""

    def to_dict(self) -> dict:
        return {
            "chip": self.chip,
            "chip_id": self.chip_id,
            "mac_address": self.mac_address,
            "flash_size": self.flash_size,
            "flash_type": self.flash_type,
            "crystal": self.crystal,
            "features": self.features,
            "raw_output": self.raw_output,
        }


@dataclass
class EfuseInfo:
    """eFuse (security) information."""

    flash_encryption: str = "disabled"
    secure_boot: str = "disabled"
    efuses: dict = field(default_factory=dict)
    raw_output: str = ""

    def to_dict(self) -> dict:
        return {
            "flash_encryption": self.flash_encryption,
            "secure_boot": self.secure_boot,
            "efuses": self.efuses,
            "raw_output": self.raw_output,
        }


@dataclass
class PartitionInfo:
    """Partition table entry."""

    name: str = ""
    type: str = ""
    subtype: str = ""
    offset: str = ""
    size: str = ""
    flags: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "subtype": self.subtype,
            "offset": self.offset,
            "size": self.size,
            "flags": self.flags,
        }


@dataclass
class FlashProgress:
    """Firmware flash progress."""

    status: str = "idle"
    progress: float = 0.0
    message: str = ""
    error: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "status": self.status,
            "progress": self.progress,
            "message": self.message,
            "error": self.error,
        }


# Flash offsets for different chip types
FLASH_OFFSETS = {
    "esp32": "0x1000",
    "esp32c3": "0x0",
    "esp32c6": "0x0",
    "esp32s2": "0x1000",
    "esp32s3": "0x0",
    "esp8266": "0x0",
}


class FirmwareFlasher:
    """Firmware flashing and chip info using esptool."""

    # Default firmware download URLs
    FIRMWARE_URLS = {
        "esp32": "https://micropython.org/resources/firmware/ESP32_GENERIC-20240602-v1.23.0.bin",
        "esp32c3": "https://micropython.org/resources/firmware/ESP32_GENERIC_C3-20240602-v1.23.0.bin",
        "esp32c6": "https://micropython.org/resources/firmware/ESP32_GENERIC_C6-20241129-v1.27.0.bin",
        "esp32s3": "https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240602-v1.23.0.bin",
    }

    def __init__(self, events: "EventBus") -> None:
        self.events = events
        self._progress = FlashProgress()
        self._process: asyncio.subprocess.Process | None = None

    def get_progress(self) -> dict:
        """Get current flash progress."""
        return self._progress.to_dict()

    async def get_chip_info(self, port: str) -> ChipInfo:
        """Get chip information using esptool."""
        info = ChipInfo()

        try:
            # Run esptool flash_id to get chip info
            cmd = [
                sys.executable, "-m", "esptool",
                "--port", port,
                "flash_id",
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )

            stdout, _ = await asyncio.wait_for(
                process.communicate(),
                timeout=30,
            )

            output = stdout.decode()
            info.raw_output = output

            # Parse chip type
            chip_match = re.search(r"Chip is (\S+)", output)
            if chip_match:
                info.chip = chip_match.group(1)

            # Parse MAC address
            mac_match = re.search(r"MAC: ([0-9a-f:]+)", output, re.IGNORECASE)
            if mac_match:
                info.mac_address = mac_match.group(1)

            # Parse flash size
            flash_match = re.search(r"(\d+)MB", output)
            if flash_match:
                info.flash_size = f"{flash_match.group(1)}MB"
            else:
                flash_match = re.search(r"Detected flash size: (\S+)", output)
                if flash_match:
                    info.flash_size = flash_match.group(1)

            # Parse crystal frequency
            crystal_match = re.search(r"Crystal is (\d+MHz)", output)
            if crystal_match:
                info.crystal = crystal_match.group(1)

            # Parse features
            features_match = re.search(r"Features: (.+)", output)
            if features_match:
                info.features = [f.strip() for f in features_match.group(1).split(",")]

            # Parse chip ID
            chip_id_match = re.search(r"Chip ID: (0x[0-9a-fA-F]+)", output)
            if chip_id_match:
                info.chip_id = chip_id_match.group(1)

            # Parse manufacturer
            mfr_match = re.search(r"Manufacturer: (\S+)", output)
            if mfr_match:
                info.flash_type = mfr_match.group(1)

            logger.info("Got chip info for %s: %s", port, info.chip)

        except asyncio.TimeoutError:
            logger.error("Timeout getting chip info for %s", port)
            info.raw_output = "Timeout - device may be busy"
        except Exception as e:
            logger.exception("Error getting chip info: %s", e)
            info.raw_output = f"Error: {e}"

        return info

    async def list_available(self) -> list[dict]:
        """List available firmware files."""
        firmware_list = []

        # List local firmware files
        firmware_dir = Path.home() / ".pulsar" / "firmware"
        if firmware_dir.exists():
            for file in firmware_dir.glob("*.bin"):
                firmware_list.append({
                    "name": file.stem,
                    "path": str(file),
                    "size": file.stat().st_size,
                    "local": True,
                })

        # Also check current directory and common locations
        cwd = Path.cwd()
        for file in cwd.glob("*.bin"):
            firmware_list.append({
                "name": file.name,
                "path": str(file),
                "size": file.stat().st_size,
                "local": True,
            })

        # Add download options
        for chip, url in self.FIRMWARE_URLS.items():
            firmware_list.append({
                "name": f"MicroPython {chip.upper()} (download)",
                "url": url,
                "chip": chip,
                "local": False,
            })

        return firmware_list

    async def erase_flash(self, port: str) -> bool:
        """Erase flash on the device."""
        self._progress = FlashProgress(
            status="erasing",
            message="Erasing flash...",
        )

        try:
            self.events.emit(
                EventType.FIRMWARE_PROGRESS,
                {"port": port, "progress": self._progress.to_dict()},
            )

            cmd = [
                sys.executable, "-m", "esptool",
                "--port", port,
                "erase_flash",
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                self._progress = FlashProgress(
                    status="erased",
                    progress=0.5,
                    message="Flash erased successfully",
                )
                self.events.emit(
                    EventType.FIRMWARE_PROGRESS,
                    {"port": port, "progress": self._progress.to_dict()},
                )
                return True
            else:
                self._progress = FlashProgress(
                    status="error",
                    error=stderr.decode() or stdout.decode(),
                )
                return False

        except Exception as e:
            self._progress = FlashProgress(
                status="error",
                error=str(e),
            )
            return False

        finally:
            self.events.emit(
                EventType.FIRMWARE_PROGRESS,
                {"port": port, "progress": self._progress.to_dict()},
            )

    def _detect_chip_type(self, firmware_path: str) -> str:
        """Try to detect chip type from firmware filename."""
        name = Path(firmware_path).name.lower()

        if "c6" in name or "esp32c6" in name:
            return "esp32c6"
        elif "c3" in name or "esp32c3" in name:
            return "esp32c3"
        elif "s3" in name or "esp32s3" in name:
            return "esp32s3"
        elif "s2" in name or "esp32s2" in name:
            return "esp32s2"
        elif "8266" in name:
            return "esp8266"
        elif "esp32" in name:
            return "esp32"

        return "auto"

    async def flash(
        self,
        port: str,
        firmware_path: str,
        chip: str = "auto",
        baud: int = 460800,
        erase_first: bool = True,
    ) -> bool:
        """Flash firmware to the device."""
        self._progress = FlashProgress(
            status="starting",
            message="Preparing to flash...",
        )

        try:
            # Verify firmware file exists
            if not Path(firmware_path).exists():
                raise FileNotFoundError(f"Firmware not found: {firmware_path}")

            self.events.emit(
                EventType.FIRMWARE_PROGRESS,
                {"port": port, "progress": self._progress.to_dict()},
            )

            # Detect chip type if auto
            detected_chip = self._detect_chip_type(firmware_path) if chip == "auto" else chip

            # Get flash offset for chip type
            flash_offset = FLASH_OFFSETS.get(detected_chip.lower(), "0x1000")
            logger.info("Using chip type: %s, flash offset: %s", detected_chip, flash_offset)

            # Erase flash first if requested
            if erase_first:
                if not await self.erase_flash(port):
                    return False

            # Flash firmware
            self._progress = FlashProgress(
                status="flashing",
                message=f"Flashing firmware (chip: {detected_chip})...",
            )

            self.events.emit(
                EventType.FIRMWARE_PROGRESS,
                {"port": port, "progress": self._progress.to_dict()},
            )

            cmd = [
                sys.executable, "-m", "esptool",
                "--port", port,
                "--baud", str(baud),
            ]

            if detected_chip != "auto":
                cmd.extend(["--chip", detected_chip])

            cmd.extend([
                "write_flash",
                "-z",
                flash_offset,
                firmware_path,
            ])

            logger.info("Running: %s", " ".join(cmd))

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )

            self._process = process

            # Monitor output for progress
            while True:
                line = await process.stdout.readline()
                if not line:
                    break

                text = line.decode().strip()
                logger.debug("esptool: %s", text)

                # Parse progress from esptool output
                if "%" in text:
                    try:
                        # Extract percentage - esptool outputs like "Writing at 0x00001000... (1 %)"
                        match = re.search(r"\((\d+)\s*%\)", text)
                        if match:
                            percent = int(match.group(1))
                            # Erase was 0-50%, flash is 50-100%
                            self._progress.progress = 0.5 + (percent / 200.0)
                            self._progress.message = text

                            self.events.emit(
                                EventType.FIRMWARE_PROGRESS,
                                {"port": port, "progress": self._progress.to_dict()},
                            )
                    except (ValueError, IndexError):
                        pass
                elif "Hash of data verified" in text:
                    self._progress.message = "Verifying..."
                    self.events.emit(
                        EventType.FIRMWARE_PROGRESS,
                        {"port": port, "progress": self._progress.to_dict()},
                    )

            await process.wait()

            if process.returncode == 0:
                self._progress = FlashProgress(
                    status="complete",
                    progress=1.0,
                    message="Firmware flashed successfully! Reset the device to boot.",
                )

                self.events.emit(
                    EventType.FIRMWARE_COMPLETE,
                    {"port": port},
                )
                return True
            else:
                self._progress = FlashProgress(
                    status="error",
                    error="Flash failed - check device connection and boot mode",
                )

                self.events.emit(
                    EventType.FIRMWARE_ERROR,
                    {"port": port, "error": self._progress.error},
                )
                return False

        except Exception as e:
            logger.exception("Flash error: %s", e)
            self._progress = FlashProgress(
                status="error",
                error=str(e),
            )

            self.events.emit(
                EventType.FIRMWARE_ERROR,
                {"port": port, "error": str(e)},
            )
            return False

        finally:
            self._process = None

    async def download_firmware(
        self,
        url: str,
        name: str | None = None,
    ) -> str:
        """Download firmware from URL."""
        import aiohttp

        firmware_dir = Path.home() / ".pulsar" / "firmware"
        firmware_dir.mkdir(parents=True, exist_ok=True)

        if name is None:
            name = url.split("/")[-1]

        dest_path = firmware_dir / name

        self._progress = FlashProgress(
            status="downloading",
            message=f"Downloading {name}...",
        )

        self.events.emit(
            EventType.FIRMWARE_PROGRESS,
            {"port": "", "progress": self._progress.to_dict()},
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise RuntimeError(f"Download failed: {response.status}")

                total = int(response.headers.get("content-length", 0))
                downloaded = 0

                with open(dest_path, "wb") as f:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total > 0:
                            self._progress.progress = downloaded / total
                            self._progress.message = f"Downloading... {downloaded // 1024}KB / {total // 1024}KB"
                            self.events.emit(
                                EventType.FIRMWARE_PROGRESS,
                                {"port": "", "progress": self._progress.to_dict()},
                            )

        self._progress = FlashProgress(
            status="downloaded",
            progress=1.0,
            message=f"Downloaded to {dest_path}",
        )

        return str(dest_path)

    async def get_efuse_info(self, port: str) -> EfuseInfo:
        """Get eFuse information (security settings)."""
        info = EfuseInfo()

        try:
            # Run espefuse summary
            cmd = [
                sys.executable, "-m", "espefuse",
                "--port", port,
                "summary",
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )

            stdout, _ = await asyncio.wait_for(
                process.communicate(),
                timeout=30,
            )

            output = stdout.decode()
            info.raw_output = output

            # Parse flash encryption status
            if "FLASH_CRYPT_CNT" in output:
                flash_enc_match = re.search(r"FLASH_CRYPT_CNT\s*=\s*(\S+)", output)
                if flash_enc_match:
                    value = flash_enc_match.group(1)
                    if value != "0x0" and value != "0":
                        info.flash_encryption = "enabled"

            # Check for SPI_BOOT_CRYPT_CNT (newer chips)
            if "SPI_BOOT_CRYPT_CNT" in output:
                enc_match = re.search(r"SPI_BOOT_CRYPT_CNT\s*=\s*(\S+)", output)
                if enc_match and enc_match.group(1) not in ("0x0", "0"):
                    info.flash_encryption = "enabled"

            # Parse secure boot status
            if "SECURE_BOOT" in output.upper():
                sb_match = re.search(r"SECURE_BOOT\w*\s*=\s*(\S+)", output, re.IGNORECASE)
                if sb_match and sb_match.group(1) not in ("0x0", "0", "False"):
                    info.secure_boot = "enabled"

            # Parse key eFuses
            efuse_patterns = [
                r"(FLASH_CRYPT_CNT)\s*=\s*(\S+)",
                r"(SECURE_BOOT_EN)\s*=\s*(\S+)",
                r"(JTAG_DISABLE)\s*=\s*(\S+)",
                r"(DOWNLOAD_DIS_ENCRYPT)\s*=\s*(\S+)",
                r"(DOWNLOAD_DIS_DECRYPT)\s*=\s*(\S+)",
                r"(DOWNLOAD_DIS_CACHE)\s*=\s*(\S+)",
                r"(DISABLE_WAFER_VERSION_MAJOR)\s*=\s*(\S+)",
            ]

            for pattern in efuse_patterns:
                match = re.search(pattern, output, re.IGNORECASE)
                if match:
                    info.efuses[match.group(1)] = match.group(2)

            logger.info("Got eFuse info for %s", port)

        except asyncio.TimeoutError:
            logger.error("Timeout getting eFuse info for %s", port)
            info.raw_output = "Timeout - espefuse not available or device busy"
        except Exception as e:
            logger.exception("Error getting eFuse info: %s", e)
            info.raw_output = f"Error: {e}"

        return info

    async def get_partitions(self, port: str) -> list[PartitionInfo]:
        """Read partition table from device."""
        partitions = []

        try:
            # First, read partition table binary from device
            partition_offset = "0x8000"
            partition_size = "0x1000"

            # Create temp file for partition data
            temp_file = Path.home() / ".pulsar" / "temp_partitions.bin"
            temp_file.parent.mkdir(parents=True, exist_ok=True)

            # Read partition table from flash
            cmd = [
                sys.executable, "-m", "esptool",
                "--port", port,
                "read_flash",
                partition_offset,
                partition_size,
                str(temp_file),
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )

            stdout, _ = await asyncio.wait_for(
                process.communicate(),
                timeout=60,
            )

            if process.returncode != 0:
                logger.error("Failed to read partitions: %s", stdout.decode())
                return partitions

            # Parse partition table binary using gen_esp32part
            parse_cmd = [
                sys.executable, "-m", "gen_esp32part",
                str(temp_file),
            ]

            try:
                parse_process = await asyncio.create_subprocess_exec(
                    *parse_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                )

                parse_stdout, _ = await asyncio.wait_for(
                    parse_process.communicate(),
                    timeout=10,
                )

                output = parse_stdout.decode()

                # Parse CSV-like output
                for line in output.split("\n"):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) >= 5:
                        partition = PartitionInfo(
                            name=parts[0],
                            type=parts[1],
                            subtype=parts[2],
                            offset=parts[3],
                            size=parts[4],
                            flags=parts[5] if len(parts) > 5 else "",
                        )
                        partitions.append(partition)

            except Exception as e:
                # If gen_esp32part not available, parse binary manually
                logger.warning("gen_esp32part not available, using basic parser: %s", e)
                partitions = self._parse_partition_binary(temp_file)

            # Clean up temp file
            try:
                temp_file.unlink()
            except Exception:
                pass

            logger.info("Got %d partitions for %s", len(partitions), port)

        except asyncio.TimeoutError:
            logger.error("Timeout reading partitions for %s", port)
        except Exception as e:
            logger.exception("Error reading partitions: %s", e)

        return partitions

    def _parse_partition_binary(self, path: Path) -> list[PartitionInfo]:
        """Parse partition table binary manually."""
        partitions = []

        try:
            with open(path, "rb") as f:
                data = f.read()

            # Partition entry is 32 bytes
            # Magic bytes: 0xAA 0x50
            offset = 0
            while offset + 32 <= len(data):
                entry = data[offset:offset + 32]

                # Check magic bytes
                if entry[0:2] != b'\xaa\x50':
                    offset += 32
                    continue

                # Parse entry
                entry_type = entry[2]
                subtype = entry[3]
                part_offset = int.from_bytes(entry[4:8], 'little')
                size = int.from_bytes(entry[8:12], 'little')
                name = entry[12:28].rstrip(b'\x00').decode('utf-8', errors='replace')
                flags = int.from_bytes(entry[28:32], 'little')

                type_names = {0: "app", 1: "data"}
                subtype_names = {
                    (0, 0): "factory", (0, 16): "ota_0", (0, 17): "ota_1",
                    (1, 0): "ota", (1, 1): "phy", (1, 2): "nvs",
                    (1, 129): "nvs_keys", (1, 130): "efuse",
                }

                partition = PartitionInfo(
                    name=name,
                    type=type_names.get(entry_type, hex(entry_type)),
                    subtype=subtype_names.get((entry_type, subtype), hex(subtype)),
                    offset=hex(part_offset),
                    size=hex(size),
                    flags=hex(flags) if flags else "",
                )
                partitions.append(partition)

                offset += 32

        except Exception as e:
            logger.exception("Error parsing partition binary: %s", e)

        return partitions

    async def read_flash(
        self,
        port: str,
        offset: str = "0x0",
        size: str = "0x400000",  # 4MB default
        output_path: str | None = None,
    ) -> str:
        """Read flash contents to file."""
        if output_path is None:
            output_dir = Path.home() / ".pulsar" / "backups"
            output_dir.mkdir(parents=True, exist_ok=True)
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = str(output_dir / f"flash_backup_{timestamp}.bin")

        self._progress = FlashProgress(
            status="reading",
            message=f"Reading flash from {offset}...",
        )

        try:
            self.events.emit(
                EventType.FIRMWARE_PROGRESS,
                {"port": port, "progress": self._progress.to_dict()},
            )

            cmd = [
                sys.executable, "-m", "esptool",
                "--port", port,
                "read_flash",
                offset,
                size,
                output_path,
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )

            self._process = process

            while True:
                line = await process.stdout.readline()
                if not line:
                    break

                text = line.decode().strip()
                logger.debug("esptool read: %s", text)

                # Parse progress
                if "%" in text:
                    match = re.search(r"\((\d+)\s*%\)", text)
                    if match:
                        percent = int(match.group(1))
                        self._progress.progress = percent / 100.0
                        self._progress.message = text

                        self.events.emit(
                            EventType.FIRMWARE_PROGRESS,
                            {"port": port, "progress": self._progress.to_dict()},
                        )

            await process.wait()

            if process.returncode == 0:
                self._progress = FlashProgress(
                    status="complete",
                    progress=1.0,
                    message=f"Flash read to {output_path}",
                )
                return output_path
            else:
                self._progress = FlashProgress(
                    status="error",
                    error="Read flash failed",
                )
                return ""

        except Exception as e:
            logger.exception("Read flash error: %s", e)
            self._progress = FlashProgress(
                status="error",
                error=str(e),
            )
            return ""

        finally:
            self._process = None
            self.events.emit(
                EventType.FIRMWARE_PROGRESS,
                {"port": port, "progress": self._progress.to_dict()},
            )

    async def verify_flash(
        self,
        port: str,
        firmware_path: str,
        offset: str = "0x0",
    ) -> bool:
        """Verify flash contents against a file."""
        self._progress = FlashProgress(
            status="verifying",
            message="Verifying flash...",
        )

        try:
            if not Path(firmware_path).exists():
                raise FileNotFoundError(f"Firmware not found: {firmware_path}")

            self.events.emit(
                EventType.FIRMWARE_PROGRESS,
                {"port": port, "progress": self._progress.to_dict()},
            )

            cmd = [
                sys.executable, "-m", "esptool",
                "--port", port,
                "verify_flash",
                offset,
                firmware_path,
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )

            stdout, _ = await asyncio.wait_for(
                process.communicate(),
                timeout=120,
            )

            output = stdout.decode()

            if process.returncode == 0 and "verify OK" in output.lower():
                self._progress = FlashProgress(
                    status="verified",
                    progress=1.0,
                    message="Flash verification successful",
                )
                return True
            else:
                self._progress = FlashProgress(
                    status="failed",
                    error="Verification failed - flash contents differ",
                )
                return False

        except asyncio.TimeoutError:
            self._progress = FlashProgress(
                status="error",
                error="Verification timeout",
            )
            return False

        except Exception as e:
            logger.exception("Verify flash error: %s", e)
            self._progress = FlashProgress(
                status="error",
                error=str(e),
            )
            return False

        finally:
            self.events.emit(
                EventType.FIRMWARE_PROGRESS,
                {"port": port, "progress": self._progress.to_dict()},
            )
