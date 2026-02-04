"""pywebview window management."""

import logging
from typing import TYPE_CHECKING

import webview

if TYPE_CHECKING:
    from core.config import Config

logger = logging.getLogger(__name__)


class JSApi:
    """JavaScript API exposed to the frontend."""

    def __init__(self, config: "Config") -> None:
        self.config = config

    def get_config(self) -> dict:
        """Get application configuration."""
        return {
            "dev_mode": self.config.dev_mode,
            "server_host": self.config.server_host,
            "server_port": self.config.server_port,
            "frontend_url": self.config.frontend_url,
        }

    def get_api_url(self) -> str:
        """Get API base URL."""
        return f"http://{self.config.server_host}:{self.config.server_port}"

    def get_ws_url(self) -> str:
        """Get WebSocket URL."""
        return f"ws://{self.config.server_host}:{self.config.server_port}/ws"


def create_window(config: "Config") -> webview.Window:
    """Create the main application window."""
    logger.info("Creating application window...")

    # Create JS API
    api = JSApi(config)

    # Determine URL to load
    if config.dev_mode:
        url = config.frontend_dev_url
        logger.info("Dev mode: loading from %s", url)
    else:
        url = f"http://{config.server_host}:{config.server_port}"
        logger.info("Production mode: loading from %s", url)

    # Create window
    window = webview.create_window(
        title=config.window_title,
        url=url,
        width=config.window_width,
        height=config.window_height,
        min_size=(config.window_min_width, config.window_min_height),
        js_api=api,
        background_color="#1e1e1e",  # VS Code dark background
    )

    logger.info("Window created")
    return window
