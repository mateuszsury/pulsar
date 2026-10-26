"""Application configuration."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Application configuration."""

    # Runtime mode
    dev_mode: bool = False
    debug: bool = False
    headless: bool = False

    # Server settings
    server_host: str = "127.0.0.1"
    server_port: int = 8765

    # Serial settings
    default_baudrate: int = 115200
    serial_timeout: float = 1.0

    # Window settings
    window_title: str = "Pulsar"
    window_width: int = 1400
    window_height: int = 900
    window_min_width: int = 800
    window_min_height: int = 600

    # Paths
    config_dir: Path = field(default_factory=lambda: Path.home() / ".pulsar")

    # Frontend URL (in dev mode, points to Vite dev server)
    frontend_dev_url: str = "http://localhost:5173"

    def __post_init__(self) -> None:
        """Initialize configuration directory."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._load_user_config()

    def _load_user_config(self) -> None:
        """Load user configuration from config file."""
        config_file = self.config_dir / "config.json"
        if config_file.exists():
            try:
                with open(config_file) as f:
                    data = json.load(f)
                for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                logger.debug("Loaded user config from %s", config_file)
            except Exception as e:
                logger.warning("Failed to load config: %s", e)

    def save(self) -> None:
        """Save current configuration to file."""
        config_file = self.config_dir / "config.json"
        data = {
            "default_baudrate": self.default_baudrate,
            "window_width": self.window_width,
            "window_height": self.window_height,
        }
        try:
            with open(config_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.debug("Saved config to %s", config_file)
        except Exception as e:
            logger.warning("Failed to save config: %s", e)

    @property
    def static_dir(self) -> Path:
        """Path to static frontend files."""
        return Path(__file__).parent.parent / "ui" / "static"

    @property
    def frontend_url(self) -> str:
        """URL for frontend (dev server or local files)."""
        if self.dev_mode:
            return self.frontend_dev_url
        return f"http://{self.server_host}:{self.server_port}"
