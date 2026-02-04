"""REST API server using aiohttp."""

import asyncio
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

from aiohttp import web

from server.websocket import WebSocketHandler

if TYPE_CHECKING:
    from core.config import Config
    from core.events import EventBus
    from serial_comm.manager import SerialManager
    from tools.flasher import FirmwareFlasher
    from tools.wifi import WiFiManager
    from tools.sync import FolderSync
    from tools.lib_manager import LibraryManager
    from lsp.manager import LSPManager

logger = logging.getLogger(__name__)


def json_response(data: Any, status: int = 200) -> web.Response:
    """Create JSON response."""
    return web.json_response(data, status=status)


def error_response(message: str, status: int = 400) -> web.Response:
    """Create error JSON response."""
    return web.json_response({"error": message}, status=status)


class APIServer:
    """REST API and WebSocket server."""

    def __init__(
        self,
        events: "EventBus",
        config: "Config",
        serial_manager: "SerialManager",
    ) -> None:
        self.events = events
        self.config = config
        self.serial_manager = serial_manager

        self._app = web.Application()
        self._runner: web.AppRunner | None = None
        self._ws_handler = WebSocketHandler(events, serial_manager)

        # Lazy-loaded tools
        self._flasher: "FirmwareFlasher | None" = None
        self._wifi_manager: "WiFiManager | None" = None
        self._sync: "FolderSync | None" = None
        self._lib_manager: "LibraryManager | None" = None
        self._lsp_manager: Optional["LSPManager"] = None

        self._setup_routes()

    def _setup_routes(self) -> None:
        """Setup API routes."""
        self._app.router.add_get("/ws", self._ws_handler.handle)

        # Port routes
        self._app.router.add_get("/api/ports", self._get_ports)

        # Device routes
        self._app.router.add_get("/api/devices", self._get_devices)
        self._app.router.add_get("/api/devices/{port}", self._get_device)
        self._app.router.add_post("/api/devices/{port}/connect", self._connect_device)
        self._app.router.add_post("/api/devices/{port}/disconnect", self._disconnect_device)
        self._app.router.add_post("/api/devices/{port}/reset", self._reset_device)
        self._app.router.add_post("/api/devices/{port}/interrupt", self._interrupt_device)

        # REPL routes
        self._app.router.add_post("/api/devices/{port}/repl", self._execute_repl)

        # File routes
        self._app.router.add_get("/api/devices/{port}/files", self._list_files)
        self._app.router.add_get("/api/devices/{port}/files/read", self._read_file)
        self._app.router.add_post("/api/devices/{port}/files/write", self._write_file)
        self._app.router.add_delete("/api/devices/{port}/files", self._delete_file)
        self._app.router.add_post("/api/devices/{port}/files/mkdir", self._mkdir)

        # Firmware routes
        self._app.router.add_get("/api/firmware/list", self._list_firmware)
        self._app.router.add_post("/api/firmware/flash", self._flash_firmware)
        self._app.router.add_get("/api/firmware/progress", self._firmware_progress)

        # WiFi routes
        self._app.router.add_get("/api/devices/{port}/wifi/scan", self._wifi_scan)
        self._app.router.add_post("/api/devices/{port}/wifi/config", self._wifi_config)
        self._app.router.add_get("/api/devices/{port}/wifi/status", self._wifi_status)

        # Logs
        self._app.router.add_get("/api/logs", self._get_logs)

        # Chip info (esptool)
        self._app.router.add_get("/api/devices/{port}/chipinfo", self._get_chip_info)
        self._app.router.add_get("/api/devices/{port}/efuse", self._get_efuse_info)
        self._app.router.add_get("/api/devices/{port}/partitions", self._get_partitions)
        self._app.router.add_post("/api/firmware/read", self._read_flash)
        self._app.router.add_post("/api/firmware/verify", self._verify_flash)
        self._app.router.add_post("/api/firmware/erase", self._erase_flash)

        # Folder sync
        self._app.router.add_post("/api/devices/{port}/sync/compare", self._sync_compare)
        self._app.router.add_post("/api/devices/{port}/sync/upload", self._sync_upload)

        # Library management
        self._app.router.add_get("/api/packages", self._list_packages)
        self._app.router.add_get("/api/packages/search", self._search_packages)
        self._app.router.add_get("/api/devices/{port}/packages", self._list_installed_packages)
        self._app.router.add_post("/api/devices/{port}/packages/install", self._install_package)
        self._app.router.add_delete("/api/devices/{port}/packages/{name}", self._uninstall_package)
        self._app.router.add_get("/api/packages/progress", self._package_progress)

        # Firmware erase
        self._app.router.add_post("/api/firmware/erase", self._erase_flash)

        # LSP endpoints
        self._app.router.add_post("/api/lsp/initialize", self._lsp_initialize)
        self._app.router.add_post("/api/lsp/completion", self._lsp_completion)
        self._app.router.add_post("/api/lsp/hover", self._lsp_hover)
        self._app.router.add_post("/api/lsp/definition", self._lsp_definition)
        self._app.router.add_post("/api/lsp/signature", self._lsp_signature)
        self._app.router.add_post("/api/lsp/didOpen", self._lsp_did_open)
        self._app.router.add_post("/api/lsp/didChange", self._lsp_did_change)
        self._app.router.add_post("/api/lsp/didClose", self._lsp_did_close)
        self._app.router.add_get("/api/lsp/status", self._lsp_status)
        self._app.router.add_post("/api/lsp/shutdown", self._lsp_shutdown)

        # Static files (for production build)
        if self.config.static_dir.exists():
            # Serve index.html for root
            self._app.router.add_get("/", self._serve_index)
            # Serve static assets
            self._app.router.add_static("/assets", self.config.static_dir / "assets")

        # CORS middleware
        self._app.middlewares.append(self._cors_middleware)

    async def _serve_index(self, request: web.Request) -> web.Response:
        """Serve index.html for SPA."""
        index_path = self.config.static_dir / "index.html"
        if index_path.exists():
            return web.FileResponse(index_path)
        return web.Response(text="Not Found", status=404)

    @web.middleware
    async def _cors_middleware(
        self,
        request: web.Request,
        handler: Any,
    ) -> web.Response:
        """Handle CORS headers."""
        if request.method == "OPTIONS":
            response = web.Response()
        else:
            try:
                response = await handler(request)
            except web.HTTPException as e:
                response = e

        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    async def start(self) -> None:
        """Start the API server."""
        await self._ws_handler.start()

        self._runner = web.AppRunner(self._app)
        await self._runner.setup()

        site = web.TCPSite(
            self._runner,
            self.config.server_host,
            self.config.server_port,
        )
        await site.start()

        logger.info(
            "API server started at http://%s:%d",
            self.config.server_host,
            self.config.server_port,
        )

    async def stop(self) -> None:
        """Stop the API server."""
        await self._ws_handler.stop()

        if self._runner:
            await self._runner.cleanup()

        logger.info("API server stopped")

    # Port endpoints

    async def _get_ports(self, request: web.Request) -> web.Response:
        """GET /api/ports - List available serial ports."""
        ports = self.serial_manager.scan_ports()
        return json_response([p.to_dict() for p in ports])

    # Device endpoints

    async def _get_devices(self, request: web.Request) -> web.Response:
        """GET /api/devices - List connected devices."""
        devices = self.serial_manager.get_devices()
        return json_response([d.info.to_dict() for d in devices])

    async def _get_device(self, request: web.Request) -> web.Response:
        """GET /api/devices/{port} - Get device details."""
        port = request.match_info["port"]
        device = self.serial_manager.get_device(port)

        if not device:
            return error_response(f"Device not found: {port}", 404)

        return json_response(device.info.to_dict())

    async def _connect_device(self, request: web.Request) -> web.Response:
        """POST /api/devices/{port}/connect - Connect to device."""
        port = request.match_info["port"]

        try:
            data = await request.json()
        except Exception:
            data = {}

        baudrate = data.get("baudrate")
        success = await self.serial_manager.connect(port, baudrate)

        if success:
            device = self.serial_manager.get_device(port)
            response_data = {"success": True, "device": device.info.to_dict()}
            logger.info("Connect response for %s: %s", port, response_data)
            return json_response(response_data)
        else:
            return error_response(f"Failed to connect to {port}", 500)

    async def _disconnect_device(self, request: web.Request) -> web.Response:
        """POST /api/devices/{port}/disconnect - Disconnect from device."""
        port = request.match_info["port"]
        await self.serial_manager.disconnect(port)
        return json_response({"success": True})

    async def _reset_device(self, request: web.Request) -> web.Response:
        """POST /api/devices/{port}/reset - Reset device."""
        port = request.match_info["port"]

        try:
            data = await request.json()
        except Exception:
            data = {}

        soft = data.get("soft", True)
        success = await self.serial_manager.reset(port, soft=soft)

        return json_response({"success": success})

    async def _interrupt_device(self, request: web.Request) -> web.Response:
        """POST /api/devices/{port}/interrupt - Send Ctrl+C."""
        port = request.match_info["port"]
        await self.serial_manager.interrupt(port)
        return json_response({"success": True})

    # REPL endpoints

    async def _execute_repl(self, request: web.Request) -> web.Response:
        """POST /api/devices/{port}/repl - Execute code."""
        port = request.match_info["port"]

        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        code = data.get("code", "")
        timeout = data.get("timeout", 30.0)

        if not code:
            return error_response("No code provided")

        result = await self.serial_manager.execute(port, code, timeout=timeout)
        return json_response(result.to_dict())

    # File endpoints

    async def _list_files(self, request: web.Request) -> web.Response:
        """GET /api/devices/{port}/files - List files."""
        port = request.match_info["port"]
        path = request.query.get("path", "/")

        try:
            files = await self.serial_manager.list_files(port, path)
            return json_response(files)
        except Exception as e:
            return error_response(str(e), 500)

    async def _read_file(self, request: web.Request) -> web.Response:
        """GET /api/devices/{port}/files/read - Read file."""
        port = request.match_info["port"]
        path = request.query.get("path")

        if not path:
            return error_response("No path provided")

        try:
            content = await self.serial_manager.read_file(port, path)
            # Try to decode as text
            try:
                text = content.decode("utf-8")
                return json_response({"content": text, "binary": False})
            except UnicodeDecodeError:
                # Return as base64
                import base64
                return json_response({
                    "content": base64.b64encode(content).decode(),
                    "binary": True,
                })
        except Exception as e:
            return error_response(str(e), 500)

    async def _write_file(self, request: web.Request) -> web.Response:
        """POST /api/devices/{port}/files/write - Write file."""
        port = request.match_info["port"]

        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        path = data.get("path")
        content = data.get("content", "")
        binary = data.get("binary", False)

        if not path:
            return error_response("No path provided")

        try:
            if binary:
                import base64
                content_bytes = base64.b64decode(content)
            else:
                content_bytes = content.encode("utf-8")

            success = await self.serial_manager.write_file(port, path, content_bytes)
            return json_response({"success": success})
        except Exception as e:
            return error_response(str(e), 500)

    async def _delete_file(self, request: web.Request) -> web.Response:
        """DELETE /api/devices/{port}/files - Delete file."""
        port = request.match_info["port"]
        path = request.query.get("path")

        if not path:
            return error_response("No path provided")

        try:
            success = await self.serial_manager.delete_file(port, path)
            return json_response({"success": success})
        except Exception as e:
            return error_response(str(e), 500)

    async def _mkdir(self, request: web.Request) -> web.Response:
        """POST /api/devices/{port}/files/mkdir - Create directory."""
        port = request.match_info["port"]

        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        path = data.get("path")

        if not path:
            return error_response("No path provided")

        try:
            success = await self.serial_manager.mkdir(port, path)
            return json_response({"success": success})
        except Exception as e:
            return error_response(str(e), 500)

    # Firmware endpoints

    async def _list_firmware(self, request: web.Request) -> web.Response:
        """GET /api/firmware/list - List available firmware."""
        if not self._flasher:
            from tools.flasher import FirmwareFlasher
            self._flasher = FirmwareFlasher(self.events)

        firmware_list = await self._flasher.list_available()
        return json_response(firmware_list)

    async def _flash_firmware(self, request: web.Request) -> web.Response:
        """POST /api/firmware/flash - Flash firmware."""
        if not self._flasher:
            from tools.flasher import FirmwareFlasher
            self._flasher = FirmwareFlasher(self.events)

        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        port = data.get("port")
        firmware_path = data.get("firmware_path")

        if not port or not firmware_path:
            return error_response("Port and firmware_path required")

        # Flash in background
        asyncio.create_task(
            self._flasher.flash(port, firmware_path)
        )

        return json_response({"success": True, "message": "Flashing started"})

    async def _firmware_progress(self, request: web.Request) -> web.Response:
        """GET /api/firmware/progress - Get flash progress."""
        if not self._flasher:
            return json_response({"progress": 0, "status": "idle"})

        return json_response(self._flasher.get_progress())

    # WiFi endpoints

    async def _wifi_scan(self, request: web.Request) -> web.Response:
        """GET /api/devices/{port}/wifi/scan - Scan WiFi networks."""
        port = request.match_info["port"]

        if not self._wifi_manager:
            from tools.wifi import WiFiManager
            self._wifi_manager = WiFiManager(self.serial_manager)

        try:
            networks = await self._wifi_manager.scan(port)
            return json_response(networks)
        except Exception as e:
            return error_response(str(e), 500)

    async def _wifi_config(self, request: web.Request) -> web.Response:
        """POST /api/devices/{port}/wifi/config - Configure WiFi."""
        port = request.match_info["port"]

        if not self._wifi_manager:
            from tools.wifi import WiFiManager
            self._wifi_manager = WiFiManager(self.serial_manager)

        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        ssid = data.get("ssid")
        password = data.get("password", "")

        if not ssid:
            return error_response("SSID required")

        try:
            success = await self._wifi_manager.configure(port, ssid, password)
            return json_response({"success": success})
        except Exception as e:
            return error_response(str(e), 500)

    async def _wifi_status(self, request: web.Request) -> web.Response:
        """GET /api/devices/{port}/wifi/status - Get WiFi status."""
        port = request.match_info["port"]

        if not self._wifi_manager:
            from tools.wifi import WiFiManager
            self._wifi_manager = WiFiManager(self.serial_manager)

        try:
            status = await self._wifi_manager.get_status(port)
            return json_response(status)
        except Exception as e:
            return error_response(str(e), 500)

    # Logs endpoint

    async def _get_logs(self, request: web.Request) -> web.Response:
        """GET /api/logs - Get application logs."""
        # TODO: Implement log buffering
        return json_response({"logs": []})

    # Chip info endpoints

    async def _get_chip_info(self, request: web.Request) -> web.Response:
        """GET /api/devices/{port}/chipinfo - Get chip info using esptool."""
        port = request.match_info["port"]

        if not self._flasher:
            from tools.flasher import FirmwareFlasher
            self._flasher = FirmwareFlasher(self.events)

        try:
            # Need to disconnect device first for esptool to work
            device = self.serial_manager.get_device(port)
            was_connected = device is not None

            if was_connected:
                await self.serial_manager.disconnect(port)

            info = await self._flasher.get_chip_info(port)

            # Reconnect if was connected
            if was_connected:
                await self.serial_manager.connect(port)

            return json_response(info.to_dict())
        except Exception as e:
            return error_response(str(e), 500)

    async def _erase_flash(self, request: web.Request) -> web.Response:
        """POST /api/firmware/erase - Erase flash."""
        if not self._flasher:
            from tools.flasher import FirmwareFlasher
            self._flasher = FirmwareFlasher(self.events)

        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        port = data.get("port")
        if not port:
            return error_response("Port required")

        # Disconnect device first
        device = self.serial_manager.get_device(port)
        if device:
            await self.serial_manager.disconnect(port)

        # Erase in background
        asyncio.create_task(self._flasher.erase_flash(port))

        return json_response({"success": True, "message": "Erasing started"})

    async def _get_efuse_info(self, request: web.Request) -> web.Response:
        """GET /api/devices/{port}/efuse - Get eFuse security info."""
        port = request.match_info["port"]

        if not self._flasher:
            from tools.flasher import FirmwareFlasher
            self._flasher = FirmwareFlasher(self.events)

        try:
            # Need to disconnect device first for esptool to work
            device = self.serial_manager.get_device(port)
            was_connected = device is not None

            if was_connected:
                await self.serial_manager.disconnect(port)

            info = await self._flasher.get_efuse_info(port)

            # Reconnect if was connected
            if was_connected:
                await self.serial_manager.connect(port)

            return json_response(info.to_dict())
        except Exception as e:
            return error_response(str(e), 500)

    async def _get_partitions(self, request: web.Request) -> web.Response:
        """GET /api/devices/{port}/partitions - Get partition table."""
        port = request.match_info["port"]

        if not self._flasher:
            from tools.flasher import FirmwareFlasher
            self._flasher = FirmwareFlasher(self.events)

        try:
            # Need to disconnect device first for esptool to work
            device = self.serial_manager.get_device(port)
            was_connected = device is not None

            if was_connected:
                await self.serial_manager.disconnect(port)

            partitions = await self._flasher.get_partitions(port)

            # Reconnect if was connected
            if was_connected:
                await self.serial_manager.connect(port)

            return json_response({
                "partitions": [p.to_dict() for p in partitions],
                "count": len(partitions),
            })
        except Exception as e:
            return error_response(str(e), 500)

    async def _read_flash(self, request: web.Request) -> web.Response:
        """POST /api/firmware/read - Read flash to file (backup)."""
        if not self._flasher:
            from tools.flasher import FirmwareFlasher
            self._flasher = FirmwareFlasher(self.events)

        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        port = data.get("port")
        offset = data.get("offset", "0x0")
        size = data.get("size", "0x400000")  # 4MB default
        output_path = data.get("output")

        if not port:
            return error_response("Port required")

        # Disconnect device first
        device = self.serial_manager.get_device(port)
        was_connected = device is not None
        if device:
            await self.serial_manager.disconnect(port)

        try:
            result = await self._flasher.read_flash(port, offset, size, output_path)

            # Reconnect if was connected
            if was_connected:
                await self.serial_manager.connect(port)

            if result:
                return json_response({
                    "success": True,
                    "path": result,
                    "message": f"Flash backup saved to {result}",
                })
            else:
                return error_response("Read flash failed")
        except Exception as e:
            if was_connected:
                await self.serial_manager.connect(port)
            return error_response(str(e), 500)

    async def _verify_flash(self, request: web.Request) -> web.Response:
        """POST /api/firmware/verify - Verify flash against file."""
        if not self._flasher:
            from tools.flasher import FirmwareFlasher
            self._flasher = FirmwareFlasher(self.events)

        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        port = data.get("port")
        firmware_path = data.get("firmware")
        offset = data.get("offset", "0x0")

        if not port:
            return error_response("Port required")
        if not firmware_path:
            return error_response("Firmware path required")

        # Disconnect device first
        device = self.serial_manager.get_device(port)
        was_connected = device is not None
        if device:
            await self.serial_manager.disconnect(port)

        try:
            success = await self._flasher.verify_flash(port, firmware_path, offset)

            # Reconnect if was connected
            if was_connected:
                await self.serial_manager.connect(port)

            return json_response({
                "success": success,
                "verified": success,
                "message": "Flash verification successful" if success else "Verification failed",
            })
        except Exception as e:
            if was_connected:
                await self.serial_manager.connect(port)
            return error_response(str(e), 500)

    # Folder sync endpoints

    async def _sync_compare(self, request: web.Request) -> web.Response:
        """POST /api/devices/{port}/sync/compare - Compare local folder with device."""
        port = request.match_info["port"]

        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        local_folder = data.get("folder")
        remote_folder = data.get("remote", "/")

        if not local_folder:
            return error_response("Folder path required")

        from pathlib import Path
        folder_path = Path(local_folder)

        if not folder_path.exists():
            return error_response(f"Folder not found: {local_folder}")

        if not self._sync:
            from tools.sync import FolderSync
            self._sync = FolderSync(self.serial_manager)

        try:
            files = await self._sync.compare_files(port, folder_path, remote_folder)
            return json_response({
                "files": [f.to_dict() for f in files],
                "to_upload": [f.path for f in files if f.needs_upload],
                "total": len(files),
                "needs_upload": sum(1 for f in files if f.needs_upload),
            })
        except Exception as e:
            logger.exception("Sync compare error: %s", e)
            return error_response(str(e), 500)

    async def _sync_upload(self, request: web.Request) -> web.Response:
        """POST /api/devices/{port}/sync/upload - Sync folder to device."""
        port = request.match_info["port"]

        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        local_folder = data.get("folder")
        remote_folder = data.get("remote", "/")
        dry_run = data.get("dry_run", False)

        if not local_folder:
            return error_response("Folder path required")

        from pathlib import Path
        folder_path = Path(local_folder)

        if not folder_path.exists():
            return error_response(f"Folder not found: {local_folder}")

        if not self._sync:
            from tools.sync import FolderSync

            # Progress callback
            def on_progress(file: str, progress: float, status: str) -> None:
                from core.events import EventType
                self.events.emit(
                    EventType.FILE_PROGRESS,
                    {"port": port, "file": file, "progress": progress, "status": status},
                    source=port,
                )

            self._sync = FolderSync(self.serial_manager, on_progress=on_progress)

        try:
            result = await self._sync.sync_folder(port, folder_path, remote_folder, dry_run)
            return json_response(result.to_dict())
        except Exception as e:
            logger.exception("Sync upload error: %s", e)
            return error_response(str(e), 500)

    # Library management endpoints

    async def _list_packages(self, request: web.Request) -> web.Response:
        """GET /api/packages - List available packages."""
        if not self._lib_manager:
            from tools.lib_manager import LibraryManager
            self._lib_manager = LibraryManager(self.serial_manager)

        try:
            packages = await self._lib_manager.list_available()
            return json_response({
                "packages": [p.to_dict() for p in packages],
                "count": len(packages),
            })
        except Exception as e:
            return error_response(str(e), 500)

    async def _search_packages(self, request: web.Request) -> web.Response:
        """GET /api/packages/search?q=query - Search for packages."""
        if not self._lib_manager:
            from tools.lib_manager import LibraryManager
            self._lib_manager = LibraryManager(self.serial_manager)

        query = request.query.get("q", "")
        if not query:
            return error_response("Query parameter 'q' required")

        try:
            packages = await self._lib_manager.search_packages(query)
            return json_response({
                "packages": [p.to_dict() for p in packages],
                "count": len(packages),
                "query": query,
            })
        except Exception as e:
            return error_response(str(e), 500)

    async def _list_installed_packages(self, request: web.Request) -> web.Response:
        """GET /api/devices/{port}/packages - List installed packages on device."""
        port = request.match_info["port"]

        if not self._lib_manager:
            from tools.lib_manager import LibraryManager
            self._lib_manager = LibraryManager(self.serial_manager)

        try:
            packages = await self._lib_manager.list_installed(port)
            return json_response({
                "packages": [p.to_dict() for p in packages],
                "count": len(packages),
            })
        except Exception as e:
            return error_response(str(e), 500)

    async def _install_package(self, request: web.Request) -> web.Response:
        """POST /api/devices/{port}/packages/install - Install a package."""
        port = request.match_info["port"]

        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        package_name = data.get("package")
        force = data.get("force", False)

        if not package_name:
            return error_response("Package name required")

        if not self._lib_manager:
            from tools.lib_manager import LibraryManager
            self._lib_manager = LibraryManager(self.serial_manager)

        try:
            # Start installation (runs async)
            asyncio.create_task(
                self._lib_manager.install_package(port, package_name, force)
            )
            return json_response({
                "success": True,
                "message": f"Installing {package_name}...",
            })
        except Exception as e:
            return error_response(str(e), 500)

    async def _uninstall_package(self, request: web.Request) -> web.Response:
        """DELETE /api/devices/{port}/packages/{name} - Uninstall a package."""
        port = request.match_info["port"]
        package_name = request.match_info["name"]

        if not self._lib_manager:
            from tools.lib_manager import LibraryManager
            self._lib_manager = LibraryManager(self.serial_manager)

        try:
            success = await self._lib_manager.uninstall_package(port, package_name)
            return json_response({
                "success": success,
                "package": package_name,
            })
        except Exception as e:
            return error_response(str(e), 500)

    async def _package_progress(self, request: web.Request) -> web.Response:
        """GET /api/packages/progress - Get installation progress."""
        if not self._lib_manager:
            from tools.lib_manager import LibraryManager
            self._lib_manager = LibraryManager(self.serial_manager)

        return json_response(self._lib_manager.get_progress())

    # LSP endpoints

    async def _get_lsp_manager(self) -> "LSPManager":
        """Get or create LSP manager."""
        if self._lsp_manager is None:
            from lsp.manager import LSPManager
            self._lsp_manager = LSPManager()
        return self._lsp_manager

    async def _lsp_initialize(self, request: web.Request) -> web.Response:
        """POST /api/lsp/initialize - Initialize LSP session."""
        try:
            data = await request.json()
        except Exception:
            data = {}

        root_uri = data.get("rootUri", "file:///")
        workspace_root = data.get("workspaceRoot")

        try:
            lsp = await self._get_lsp_manager()

            # Start LSP if not running
            if not lsp.is_running:
                success = await lsp.start(
                    Path(workspace_root) if workspace_root else None
                )
                if not success:
                    return error_response("Failed to start Pyright LSP", 500)

            # Initialize session
            if not lsp.is_initialized:
                result = await lsp.initialize(root_uri)
                return json_response({
                    "success": True,
                    "capabilities": result.get("capabilities", {}),
                })
            else:
                return json_response({
                    "success": True,
                    "capabilities": {},
                    "message": "Already initialized",
                })

        except Exception as e:
            logger.exception("LSP initialize error: %s", e)
            return error_response(str(e), 500)

    async def _lsp_completion(self, request: web.Request) -> web.Response:
        """POST /api/lsp/completion - Get completions at position."""
        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        uri = data.get("uri")
        line = data.get("line", 0)
        character = data.get("character", 0)

        if not uri:
            return error_response("URI required")

        try:
            lsp = await self._get_lsp_manager()
            if not lsp.is_initialized:
                return error_response("LSP not initialized", 400)

            result = await lsp.completion(uri, line, character)
            return json_response({"items": result})

        except Exception as e:
            logger.exception("LSP completion error: %s", e)
            return error_response(str(e), 500)

    async def _lsp_hover(self, request: web.Request) -> web.Response:
        """POST /api/lsp/hover - Get hover info at position."""
        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        uri = data.get("uri")
        line = data.get("line", 0)
        character = data.get("character", 0)

        if not uri:
            return error_response("URI required")

        try:
            lsp = await self._get_lsp_manager()
            if not lsp.is_initialized:
                return error_response("LSP not initialized", 400)

            result = await lsp.hover(uri, line, character)
            return json_response({"hover": result})

        except Exception as e:
            logger.exception("LSP hover error: %s", e)
            return error_response(str(e), 500)

    async def _lsp_definition(self, request: web.Request) -> web.Response:
        """POST /api/lsp/definition - Get definition locations."""
        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        uri = data.get("uri")
        line = data.get("line", 0)
        character = data.get("character", 0)

        if not uri:
            return error_response("URI required")

        try:
            lsp = await self._get_lsp_manager()
            if not lsp.is_initialized:
                return error_response("LSP not initialized", 400)

            result = await lsp.definition(uri, line, character)
            return json_response({"locations": result})

        except Exception as e:
            logger.exception("LSP definition error: %s", e)
            return error_response(str(e), 500)

    async def _lsp_signature(self, request: web.Request) -> web.Response:
        """POST /api/lsp/signature - Get signature help."""
        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        uri = data.get("uri")
        line = data.get("line", 0)
        character = data.get("character", 0)

        if not uri:
            return error_response("URI required")

        try:
            lsp = await self._get_lsp_manager()
            if not lsp.is_initialized:
                return error_response("LSP not initialized", 400)

            result = await lsp.signature_help(uri, line, character)
            return json_response({"signatureHelp": result})

        except Exception as e:
            logger.exception("LSP signature error: %s", e)
            return error_response(str(e), 500)

    async def _lsp_did_open(self, request: web.Request) -> web.Response:
        """POST /api/lsp/didOpen - Notify document opened."""
        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        uri = data.get("uri")
        content = data.get("content", "")
        language_id = data.get("languageId", "python")

        if not uri:
            return error_response("URI required")

        try:
            lsp = await self._get_lsp_manager()
            if not lsp.is_initialized:
                return error_response("LSP not initialized", 400)

            await lsp.did_open(uri, content, language_id)
            return json_response({"success": True})

        except Exception as e:
            logger.exception("LSP didOpen error: %s", e)
            return error_response(str(e), 500)

    async def _lsp_did_change(self, request: web.Request) -> web.Response:
        """POST /api/lsp/didChange - Notify document changed."""
        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        uri = data.get("uri")
        content = data.get("content", "")
        version = data.get("version", 1)

        if not uri:
            return error_response("URI required")

        try:
            lsp = await self._get_lsp_manager()
            if not lsp.is_initialized:
                return error_response("LSP not initialized", 400)

            await lsp.did_change(uri, content, version)
            return json_response({"success": True})

        except Exception as e:
            logger.exception("LSP didChange error: %s", e)
            return error_response(str(e), 500)

    async def _lsp_did_close(self, request: web.Request) -> web.Response:
        """POST /api/lsp/didClose - Notify document closed."""
        try:
            data = await request.json()
        except Exception:
            return error_response("Invalid JSON body")

        uri = data.get("uri")

        if not uri:
            return error_response("URI required")

        try:
            lsp = await self._get_lsp_manager()
            if not lsp.is_initialized:
                return error_response("LSP not initialized", 400)

            await lsp.did_close(uri)
            return json_response({"success": True})

        except Exception as e:
            logger.exception("LSP didClose error: %s", e)
            return error_response(str(e), 500)

    async def _lsp_status(self, request: web.Request) -> web.Response:
        """GET /api/lsp/status - Get LSP status."""
        if self._lsp_manager is None:
            return json_response({
                "running": False,
                "initialized": False,
            })

        return json_response({
            "running": self._lsp_manager.is_running,
            "initialized": self._lsp_manager.is_initialized,
        })

    async def _lsp_shutdown(self, request: web.Request) -> web.Response:
        """POST /api/lsp/shutdown - Shutdown LSP server."""
        try:
            if self._lsp_manager:
                await self._lsp_manager.shutdown()
                self._lsp_manager = None

            return json_response({"success": True})

        except Exception as e:
            logger.exception("LSP shutdown error: %s", e)
            return error_response(str(e), 500)
