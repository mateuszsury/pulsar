#!/usr/bin/env python3
"""Build script for Pulsar using PyInstaller."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent
SRC_DIR = ROOT_DIR / "src"
FRONTEND_DIR = ROOT_DIR / "frontend"
STATIC_DIR = SRC_DIR / "ui" / "static"
DIST_DIR = ROOT_DIR / "dist"
ASSETS_DIR = ROOT_DIR / "assets"
STUBS_DIR = ROOT_DIR / "stubs"


def build_frontend() -> bool:
    """Build the React frontend."""
    print("\n=== Building Frontend ===\n")

    # Check if npm is available
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except FileNotFoundError:
        print("ERROR: npm not found. Please install Node.js")
        return False

    # Install dependencies
    print("Installing frontend dependencies...")
    subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, check=True)

    # Build
    print("Building frontend...")
    subprocess.run(["npm", "run", "build"], cwd=FRONTEND_DIR, check=True)

    # Verify output
    if not STATIC_DIR.exists() or not (STATIC_DIR / "index.html").exists():
        print("ERROR: Frontend build failed - no output found")
        return False

    print(f"Frontend built to {STATIC_DIR}")
    return True


def build_python() -> bool:
    """Build Python backend with PyInstaller."""
    print("\n=== Building Python Backend with PyInstaller ===\n")

    # Clean dist directory
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    # Check if static files exist
    if not STATIC_DIR.exists():
        print("ERROR: Static files not found. Run frontend build first.")
        return False

    # Icon path
    icon_path = ASSETS_DIR / "icon.ico"
    icon_arg = f"--icon={icon_path}" if icon_path.exists() else ""

    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=Pulsar",
        "--onefile",
        "--windowed",  # No console window
        "--noconfirm",
        f"--distpath={DIST_DIR}",
        f"--workpath={DIST_DIR / 'build'}",
        f"--specpath={DIST_DIR}",
        # Add the src directory as a path
        f"--paths={SRC_DIR}",
        # Add data files
        f"--add-data={STATIC_DIR};ui/static",
        # Add MicroPython stubs for LSP
        f"--add-data={STUBS_DIR};stubs",
        # Include internal packages from src
        "--hidden-import=core",
        "--hidden-import=core.app",
        "--hidden-import=core.config",
        "--hidden-import=core.events",
        "--hidden-import=server",
        "--hidden-import=server.api",
        "--hidden-import=server.websocket",
        "--hidden-import=serial_manager",
        "--hidden-import=serial_manager.manager",
        "--hidden-import=serial_manager.device",
        "--hidden-import=serial_manager.repl",
        "--hidden-import=serial_manager.file_transfer",
        "--hidden-import=serial_manager.discovery",
        "--hidden-import=mcp_impl",
        "--hidden-import=mcp_impl.server",
        "--hidden-import=mcp_impl.tools",
        "--hidden-import=mcp_impl.config_generator",
        "--hidden-import=tools",
        "--hidden-import=tools.flasher",
        "--hidden-import=tools.wifi",
        "--hidden-import=tools.sync",
        "--hidden-import=tools.lib_manager",
        "--hidden-import=ui",
        "--hidden-import=ui.window",
        # LSP module
        "--hidden-import=lsp",
        "--hidden-import=lsp.manager",
        "--hidden-import=lsp.protocol",
        # Hidden imports for external packages
        "--hidden-import=aiohttp",
        "--hidden-import=aiohttp.web",
        "--hidden-import=aiofiles",
        "--hidden-import=webview",
        "--hidden-import=webview.platforms.winforms",
        "--hidden-import=serial",
        "--hidden-import=serial.tools",
        "--hidden-import=serial.tools.list_ports",
        "--hidden-import=serial_asyncio",
        "--hidden-import=esptool",
        "--hidden-import=mcp",
        "--hidden-import=pydantic",
        "--hidden-import=clr_loader",
        "--hidden-import=pythonnet",
        "--hidden-import=pyright",
        # Collect all submodules for critical packages
        "--collect-all=webview",
        "--collect-all=aiohttp",
        "--collect-all=esptool",
        "--collect-all=serial",
        "--collect-all=clr_loader",
        "--collect-all=pyright",
        # Entry point
        str(SRC_DIR / "main.py"),
    ]

    if icon_arg:
        cmd.insert(4, icon_arg)

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT_DIR)

    if result.returncode != 0:
        print("ERROR: PyInstaller build failed")
        return False

    exe_path = DIST_DIR / "Pulsar.exe"
    if exe_path.exists():
        print(f"\nBuild complete: {exe_path}")
        print(f"Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        return True

    print("ERROR: Output executable not found")
    return False


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Build Pulsar with PyInstaller")
    parser.add_argument("--skip-frontend", action="store_true", help="Skip frontend build")
    parser.add_argument("--console", action="store_true", help="Keep console window for debugging")
    args = parser.parse_args()

    # Build frontend
    if not args.skip_frontend:
        if not build_frontend():
            return 1

    # Build Python
    if not build_python():
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
