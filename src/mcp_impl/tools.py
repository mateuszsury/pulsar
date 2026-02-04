"""MCP tool definitions for ESP32 operations."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class MCPTools:
    """MCP tool implementations for ESP32 operations."""

    def __init__(self, serial_manager: Any) -> None:
        self.serial_manager = serial_manager

    # Port operations

    async def list_ports(self) -> list[dict]:
        """List available serial ports."""
        ports = self.serial_manager.scan_ports()
        return [p.to_dict() for p in ports]

    async def list_esp32_ports(self) -> list[dict]:
        """List ESP32 devices only."""
        ports = self.serial_manager.scan_esp32_ports()
        return [p.to_dict() for p in ports]

    # Connection operations

    async def connect(
        self,
        port: str,
        baudrate: int = 115200,
    ) -> dict:
        """Connect to a device."""
        success = await self.serial_manager.connect(port, baudrate)
        if success:
            device = self.serial_manager.get_device(port)
            return {"success": True, "device": device.info.to_dict()}
        return {"success": False, "error": "Failed to connect"}

    async def disconnect(self, port: str) -> dict:
        """Disconnect from a device."""
        await self.serial_manager.disconnect(port)
        return {"success": True}

    async def get_device_info(self, port: str) -> dict:
        """Get device information."""
        device = self.serial_manager.get_device(port)
        if device:
            return device.info.to_dict()
        return {"error": f"Device not found: {port}"}

    async def list_devices(self) -> list[dict]:
        """List all connected devices."""
        devices = self.serial_manager.get_devices()
        return [d.info.to_dict() for d in devices]

    # REPL operations

    async def execute(
        self,
        port: str,
        code: str,
        timeout: float = 30.0,
    ) -> dict:
        """Execute Python code on device."""
        result = await self.serial_manager.execute(port, code, timeout=timeout)
        return result.to_dict()

    async def interrupt(self, port: str) -> dict:
        """Send Ctrl+C to interrupt execution."""
        await self.serial_manager.interrupt(port)
        return {"success": True}

    async def reset(self, port: str, soft: bool = True) -> dict:
        """Reset the device."""
        success = await self.serial_manager.reset(port, soft=soft)
        return {"success": success}

    # File operations

    async def list_files(self, port: str, path: str = "/") -> list[dict]:
        """List files in a directory."""
        return await self.serial_manager.list_files(port, path)

    async def read_file(self, port: str, path: str) -> dict:
        """Read a file from the device."""
        try:
            content = await self.serial_manager.read_file(port, path)
            try:
                text = content.decode("utf-8")
                return {"content": text, "binary": False, "size": len(content)}
            except UnicodeDecodeError:
                import base64
                return {
                    "content": base64.b64encode(content).decode(),
                    "binary": True,
                    "size": len(content),
                }
        except Exception as e:
            return {"error": str(e)}

    async def write_file(
        self,
        port: str,
        path: str,
        content: str,
        binary: bool = False,
    ) -> dict:
        """Write a file to the device."""
        try:
            if binary:
                import base64
                content_bytes = base64.b64decode(content)
            else:
                content_bytes = content.encode("utf-8")

            success = await self.serial_manager.write_file(port, path, content_bytes)
            return {"success": success}
        except Exception as e:
            return {"error": str(e)}

    async def delete_file(self, port: str, path: str) -> dict:
        """Delete a file from the device."""
        success = await self.serial_manager.delete_file(port, path)
        return {"success": success}

    async def mkdir(self, port: str, path: str) -> dict:
        """Create a directory on the device."""
        success = await self.serial_manager.mkdir(port, path)
        return {"success": success}

    async def upload_file(
        self,
        port: str,
        local_path: str,
        remote_path: str,
    ) -> dict:
        """Upload a file from local filesystem to device."""
        from pathlib import Path

        try:
            local = Path(local_path)
            if not local.exists():
                return {"error": f"Local file not found: {local_path}"}

            content = local.read_bytes()
            success = await self.serial_manager.write_file(port, remote_path, content)
            return {"success": success, "size": len(content)}
        except Exception as e:
            return {"error": str(e)}

    async def download_file(
        self,
        port: str,
        remote_path: str,
        local_path: str,
    ) -> dict:
        """Download a file from device to local filesystem."""
        from pathlib import Path

        try:
            content = await self.serial_manager.read_file(port, remote_path)
            local = Path(local_path)
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_bytes(content)
            return {"success": True, "size": len(content)}
        except Exception as e:
            return {"error": str(e)}

    # Monitoring

    async def get_logs(self, port: str, limit: int = 100) -> dict:
        """Get device output logs."""
        device = self.serial_manager.get_device(port)
        if not device:
            return {"error": f"Device not found: {port}"}

        output = device.get_output()
        lines = output.split("\n")
        if limit > 0:
            lines = lines[-limit:]

        return {"logs": lines}

    async def watch_logs(
        self,
        port: str,
        duration: int = 30,
        filter_pattern: str = "",
    ) -> dict:
        """Watch logs for a specified duration."""
        import asyncio

        device = self.serial_manager.get_device(port)
        if not device:
            return {"error": f"Device not found: {port}"}

        # Capture output for the specified duration
        start_output = device.get_output()
        await asyncio.sleep(duration)
        end_output = device.get_output()

        # Get new output since start
        if start_output and end_output.startswith(start_output):
            new_output = end_output[len(start_output):]
        else:
            new_output = end_output

        lines = new_output.split("\n")

        # Filter if pattern provided
        if filter_pattern:
            import re
            pattern = re.compile(filter_pattern, re.IGNORECASE)
            lines = [line for line in lines if pattern.search(line)]

        return {
            "logs": lines,
            "duration": duration,
            "filtered": bool(filter_pattern),
            "line_count": len(lines),
        }

    async def get_wifi_status(self, port: str) -> dict:
        """Get WiFi connection status from device."""
        code = """
import network
import json

result = {}

# Station interface
sta = network.WLAN(network.STA_IF)
result['sta_active'] = sta.active()
result['sta_connected'] = sta.isconnected()
if sta.isconnected():
    result['sta_config'] = sta.ifconfig()
    try:
        result['sta_rssi'] = sta.status('rssi')
    except:
        pass

# Access point interface
try:
    ap = network.WLAN(network.AP_IF)
    result['ap_active'] = ap.active()
    if ap.active():
        result['ap_config'] = ap.ifconfig()
        result['ap_essid'] = ap.config('essid')
except:
    pass

print(json.dumps(result))
"""
        result = await self.serial_manager.execute(port, code, timeout=10)
        if result.output:
            try:
                import json
                data = json.loads(result.output.strip())
                return data
            except Exception:
                pass
        return {"error": result.error or "Failed to get WiFi status"}

    async def get_chip_info(self, port: str) -> dict:
        """Get chip information using esptool."""
        from tools.flasher import FirmwareFlasher

        # Need temporary event bus for flasher
        class DummyEvents:
            def emit(self, *args, **kwargs): pass

        flasher = FirmwareFlasher(DummyEvents())

        # Disconnect device first for esptool to work
        device = self.serial_manager.get_device(port)
        was_connected = device is not None

        try:
            if was_connected:
                await self.serial_manager.disconnect(port)

            info = await flasher.get_chip_info(port)

            return info.to_dict()
        finally:
            if was_connected:
                await self.serial_manager.connect(port)

    async def sync_folder(
        self,
        port: str,
        local_path: str,
        remote_path: str = "/",
        dry_run: bool = False,
    ) -> dict:
        """Sync a local folder to the device."""
        from pathlib import Path
        from tools.sync import FolderSync

        folder = Path(local_path)
        if not folder.exists():
            return {"error": f"Local folder not found: {local_path}"}

        sync = FolderSync(self.serial_manager)

        try:
            # Compare files
            files = await sync.compare_files(port, folder, remote_path)

            to_upload = [f for f in files if f.needs_upload]

            if dry_run:
                return {
                    "dry_run": True,
                    "total_files": len(files),
                    "to_upload": len(to_upload),
                    "files": [f.to_dict() for f in to_upload],
                }

            # Upload files that need updating
            uploaded = []
            errors = []

            for file in to_upload:
                try:
                    local_file = folder / file.path
                    remote_file = f"{remote_path}/{file.path}".replace("//", "/")

                    content = local_file.read_bytes()
                    success = await self.serial_manager.write_file(port, remote_file, content)

                    if success:
                        uploaded.append(file.path)
                    else:
                        errors.append({"path": file.path, "error": "Write failed"})
                except Exception as e:
                    errors.append({"path": file.path, "error": str(e)})

            return {
                "success": len(errors) == 0,
                "uploaded": len(uploaded),
                "errors": errors,
                "files": uploaded,
            }
        except Exception as e:
            return {"error": str(e)}


def get_tool_definitions() -> list[dict]:
    """Get MCP tool definitions."""
    return [
        {
            "name": "list_ports",
            "description": "List all available serial ports on the system",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "list_esp32_ports",
            "description": "List only ESP32 devices (filters by known USB chip VIDs)",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "connect",
            "description": "Connect to a MicroPython device on the specified port",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {
                        "type": "string",
                        "description": "Serial port (e.g., COM4 on Windows, /dev/ttyUSB0 on Linux)",
                    },
                    "baudrate": {
                        "type": "integer",
                        "description": "Baud rate (default: 115200)",
                        "default": 115200,
                    },
                },
                "required": ["port"],
            },
        },
        {
            "name": "disconnect",
            "description": "Disconnect from a device",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                },
                "required": ["port"],
            },
        },
        {
            "name": "list_devices",
            "description": "List all currently connected devices",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "get_device_info",
            "description": "Get detailed information about a connected device",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                },
                "required": ["port"],
            },
        },
        {
            "name": "execute",
            "description": "Execute Python code on a MicroPython device",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                    "code": {
                        "type": "string",
                        "description": "Python code to execute",
                    },
                    "timeout": {
                        "type": "number",
                        "description": "Execution timeout in seconds",
                        "default": 30.0,
                    },
                },
                "required": ["port", "code"],
            },
        },
        {
            "name": "interrupt",
            "description": "Send Ctrl+C to interrupt running code on a device",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                },
                "required": ["port"],
            },
        },
        {
            "name": "reset",
            "description": "Reset the MicroPython device",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                    "soft": {
                        "type": "boolean",
                        "description": "Soft reset (True) or hard reset (False)",
                        "default": True,
                    },
                },
                "required": ["port"],
            },
        },
        {
            "name": "list_files",
            "description": "List files and directories on the device",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                    "path": {
                        "type": "string",
                        "description": "Directory path",
                        "default": "/",
                    },
                },
                "required": ["port"],
            },
        },
        {
            "name": "read_file",
            "description": "Read a file from the device",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                    "path": {
                        "type": "string",
                        "description": "File path on device",
                    },
                },
                "required": ["port", "path"],
            },
        },
        {
            "name": "write_file",
            "description": "Write a file to the device",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                    "path": {
                        "type": "string",
                        "description": "File path on device",
                    },
                    "content": {
                        "type": "string",
                        "description": "File content (text or base64 if binary)",
                    },
                    "binary": {
                        "type": "boolean",
                        "description": "Is content base64-encoded binary?",
                        "default": False,
                    },
                },
                "required": ["port", "path", "content"],
            },
        },
        {
            "name": "delete_file",
            "description": "Delete a file from the device",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                    "path": {
                        "type": "string",
                        "description": "File path on device",
                    },
                },
                "required": ["port", "path"],
            },
        },
        {
            "name": "mkdir",
            "description": "Create a directory on the device",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                    "path": {
                        "type": "string",
                        "description": "Directory path to create",
                    },
                },
                "required": ["port", "path"],
            },
        },
        {
            "name": "upload_file",
            "description": "Upload a local file to the device",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                    "local_path": {
                        "type": "string",
                        "description": "Path to local file",
                    },
                    "remote_path": {
                        "type": "string",
                        "description": "Destination path on device",
                    },
                },
                "required": ["port", "local_path", "remote_path"],
            },
        },
        {
            "name": "download_file",
            "description": "Download a file from the device to local filesystem",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                    "remote_path": {
                        "type": "string",
                        "description": "File path on device",
                    },
                    "local_path": {
                        "type": "string",
                        "description": "Destination path on local filesystem",
                    },
                },
                "required": ["port", "remote_path", "local_path"],
            },
        },
        {
            "name": "get_logs",
            "description": "Get recent output logs from a device",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of lines to return",
                        "default": 100,
                    },
                },
                "required": ["port"],
            },
        },
        {
            "name": "watch_logs",
            "description": "Watch device output for a specified duration (useful for monitoring real-time events)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                    "duration": {
                        "type": "integer",
                        "description": "How long to watch in seconds",
                        "default": 30,
                    },
                    "filter_pattern": {
                        "type": "string",
                        "description": "Optional regex pattern to filter output",
                        "default": "",
                    },
                },
                "required": ["port"],
            },
        },
        {
            "name": "get_wifi_status",
            "description": "Get WiFi connection status including IP address, RSSI, and AP info",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                },
                "required": ["port"],
            },
        },
        {
            "name": "get_chip_info",
            "description": "Get ESP chip information using esptool (chip type, MAC, flash size, etc.)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                },
                "required": ["port"],
            },
        },
        {
            "name": "sync_folder",
            "description": "Sync a local folder to the device (only uploads changed files)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Serial port"},
                    "local_path": {
                        "type": "string",
                        "description": "Local folder path to sync from",
                    },
                    "remote_path": {
                        "type": "string",
                        "description": "Remote folder path on device",
                        "default": "/",
                    },
                    "dry_run": {
                        "type": "boolean",
                        "description": "If true, only show what would be uploaded",
                        "default": False,
                    },
                },
                "required": ["port", "local_path"],
            },
        },
    ]
