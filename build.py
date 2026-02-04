#!/usr/bin/env python3
"""Build script for Pulsar - creates single .exe with Nuitka."""

import argparse
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


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and print output."""
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=cwd, check=check)


def build_frontend() -> bool:
    """Build the React frontend."""
    print("\n=== Building Frontend ===\n")

    # Check if npm is available
    try:
        run(["npm", "--version"], check=True)
    except FileNotFoundError:
        print("ERROR: npm not found. Please install Node.js")
        return False

    # Install dependencies
    print("Installing frontend dependencies...")
    run(["npm", "install"], cwd=FRONTEND_DIR)

    # Build
    print("Building frontend...")
    run(["npm", "run", "build"], cwd=FRONTEND_DIR)

    # Verify output
    if not STATIC_DIR.exists() or not (STATIC_DIR / "index.html").exists():
        print("ERROR: Frontend build failed - no output found")
        return False

    print(f"Frontend built to {STATIC_DIR}")
    return True


def build_python(
    onefile: bool = True,
    console: bool = False,
    icon: Path | None = None,
) -> bool:
    """Build Python backend with Nuitka."""
    print("\n=== Building Python Backend ===\n")

    # Ensure Nuitka is installed
    try:
        result = subprocess.run(
            [sys.executable, "-m", "nuitka", "--version"],
            capture_output=True,
            text=True,
        )
        print(f"Nuitka: {result.stdout.strip().split()[0] if result.stdout else 'installed'}")
    except Exception:
        print("Installing Nuitka...")
        run([sys.executable, "-m", "pip", "install", "nuitka", "ordered-set", "zstandard"])

    # Prepare output directory
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    # Build command
    cmd = [
        sys.executable,
        "-m", "nuitka",
        "--standalone",
        f"--output-dir={DIST_DIR}",
        "--assume-yes-for-downloads",
        "--python-flag=no_site",
        "--python-flag=no_docstrings",
        "--enable-plugin=anti-bloat",
        "--noinclude-pytest-mode=nofollow",
        "--noinclude-setuptools-mode=nofollow",
        "--noinclude-custom-mode=setuptools:nofollow",
        # Exclude unused webview platforms
        "--nofollow-import-to=webview.platforms.android",
        "--nofollow-import-to=webview.platforms.cocoa",
        "--nofollow-import-to=webview.platforms.gtk",
        "--nofollow-import-to=webview.platforms.qt",
        # Include packages
        "--include-package=aiohttp",
        "--include-package=webview.platforms.winforms",
        "--include-package=serial",
        "--include-package=serial_asyncio",
        "--include-package=esptool",
        "--include-package=mcp",
        "--include-package=pydantic",
        "--include-package=aiofiles",
        # Include data files
        f"--include-data-dir={STATIC_DIR}=ui/static",
    ]

    if onefile:
        cmd.append("--onefile")

    if not console:
        cmd.append("--windows-disable-console")

    if icon and icon.exists():
        cmd.append(f"--windows-icon-from-ico={icon}")

    # Add company info
    cmd.extend([
        "--product-name=Pulsar",
        "--product-version=0.1.0",
        "--file-description=Pulsar - Signal Your Code to Life. MicroPython/ESP32 IDE",
        "--copyright=MIT License",
    ])

    # Entry point
    cmd.append(str(SRC_DIR / "main.py"))

    # Run Nuitka
    print("Compiling with Nuitka...")
    result = run(cmd, check=False)

    if result.returncode != 0:
        print("ERROR: Nuitka compilation failed")
        return False

    # Rename output
    exe_name = "main.exe" if sys.platform == "win32" else "main"
    final_name = "Pulsar.exe" if sys.platform == "win32" else "Pulsar"

    if onefile:
        output = DIST_DIR / exe_name
        final = DIST_DIR / final_name
    else:
        output = DIST_DIR / "main.dist" / exe_name
        final = DIST_DIR / "main.dist" / final_name

    if output.exists():
        shutil.move(output, final)
        print(f"\nBuild complete: {final}")
        print(f"Size: {final.stat().st_size / (1024*1024):.1f} MB")
        return True

    print("ERROR: Output executable not found")
    return False


def clean() -> None:
    """Clean build artifacts."""
    print("\n=== Cleaning ===\n")

    dirs_to_clean = [
        DIST_DIR,
        STATIC_DIR,
        ROOT_DIR / "build",
        ROOT_DIR / "__pycache__",
        SRC_DIR / "__pycache__",
    ]

    for d in dirs_to_clean:
        if d.exists():
            print(f"Removing {d}")
            shutil.rmtree(d)

    print("Clean complete")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Build Pulsar")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean build artifacts",
    )
    parser.add_argument(
        "--frontend-only",
        action="store_true",
        help="Only build frontend",
    )
    parser.add_argument(
        "--python-only",
        action="store_true",
        help="Only build Python (skip frontend)",
    )
    parser.add_argument(
        "--no-onefile",
        action="store_true",
        help="Don't create single .exe file",
    )
    parser.add_argument(
        "--console",
        action="store_true",
        help="Keep console window (for debugging)",
    )
    parser.add_argument(
        "--icon",
        type=Path,
        default=ASSETS_DIR / "icon.ico",
        help="Path to icon file",
    )

    args = parser.parse_args()

    if args.clean:
        clean()
        return 0

    success = True

    # Build frontend
    if not args.python_only:
        success = build_frontend()
        if not success:
            return 1

        if args.frontend_only:
            return 0

    # Build Python
    if not args.frontend_only:
        success = build_python(
            onefile=not args.no_onefile,
            console=args.console,
            icon=args.icon if args.icon.exists() else None,
        )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
