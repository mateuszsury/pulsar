"""Main entry point for Pulsar application."""

import argparse
import asyncio
import logging
import sys
import os
from pathlib import Path


def _is_frozen():
    """Check if running as a PyInstaller frozen executable."""
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


# Standalone source execution and installed console entry points share imports.
if __name__ == "__main__" and not _is_frozen():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pulsar.core.app import Application
from pulsar.core.config import Config


def setup_logging(debug: bool = False) -> None:
    """Configure logging for the application."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="pulsar",
        description="Pulsar - Signal Your Code to Life. Desktop IDE for MicroPython/ESP32 development",
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Run in development mode (frontend served from Vite dev server)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="HTTP server port (default: 8765)",
    )
    parser.add_argument(
        "--no-window",
        action="store_true",
        help="Run without pywebview window (API server only)",
    )
    return parser.parse_args()


def main() -> int:
    """Application entry point."""
    args = parse_args()
    setup_logging(args.debug)

    logger = logging.getLogger("pulsar")
    logger.info("Starting Pulsar...")

    config = Config(
        dev_mode=args.dev,
        debug=args.debug,
        server_port=args.port,
        headless=args.no_window,
    )

    app = Application(config)

    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.exception("Fatal error: %s", e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
