# -*- mode: python ; coding: utf-8 -*-
"""
Pulsar - ESP32 & MicroPython IDE
PyInstaller Specification File

Author: Mateusz Sury
License: MIT

This spec file configures PyInstaller to build Pulsar as a single
Windows executable with all dependencies bundled.

Usage:
    pyinstaller Pulsar.spec --clean --noconfirm

Output:
    dist/Pulsar.exe (~45-50 MB)
"""

from PyInstaller.utils.hooks import collect_all, collect_submodules
import sys
import os

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

# Get the directory containing this spec file
SPEC_DIR = os.path.dirname(os.path.abspath(SPEC))

# Source directories
SRC_DIR = os.path.join(SPEC_DIR, 'src')
STATIC_DIR = os.path.join(SRC_DIR, 'ui', 'static')
STUBS_DIR = os.path.join(SPEC_DIR, 'stubs')
ASSETS_DIR = os.path.join(SPEC_DIR, 'assets')

# =============================================================================
# DATA FILES
# =============================================================================

# Files/directories to bundle with the application
datas = [
    # Frontend static files (React build output)
    (STATIC_DIR, 'ui/static'),

    # MicroPython type stubs for LSP
    (STUBS_DIR, 'stubs'),
]

# =============================================================================
# BINARY FILES
# =============================================================================

binaries = []

# =============================================================================
# HIDDEN IMPORTS
# =============================================================================

# Modules that PyInstaller can't detect automatically
hiddenimports = [
    # -------------------------------------------------------------------------
    # Internal Application Modules
    # -------------------------------------------------------------------------
    # Core
    'core',
    'core.app',
    'core.config',
    'core.events',

    # Server
    'server',
    'server.api',
    'server.websocket',

    # Serial Manager
    'serial_manager',
    'serial_manager.manager',
    'serial_manager.device',
    'serial_manager.repl',
    'serial_manager.file_transfer',
    'serial_manager.discovery',

    # MCP Integration
    'mcp_impl',
    'mcp_impl.server',
    'mcp_impl.tools',
    'mcp_impl.config_generator',

    # Tools
    'tools',
    'tools.flasher',
    'tools.wifi',
    'tools.sync',
    'tools.lib_manager',

    # UI
    'ui',
    'ui.window',

    # LSP
    'lsp',
    'lsp.manager',
    'lsp.protocol',

    # -------------------------------------------------------------------------
    # External Dependencies
    # -------------------------------------------------------------------------
    # Web Framework
    'aiohttp',
    'aiohttp.web',
    'aiofiles',

    # Desktop Window
    'webview',
    'webview.platforms.winforms',

    # Serial Communication
    'serial',
    'serial.tools',
    'serial.tools.list_ports',
    'serial_asyncio',

    # ESP32 Tools
    'esptool',

    # MCP SDK
    'mcp',

    # Data Validation
    'pydantic',

    # .NET Integration (for pywebview on Windows)
    'clr_loader',
    'pythonnet',

    # Language Server
    'pyright',
]

# =============================================================================
# COLLECT ALL - Packages that need complete collection
# =============================================================================

# These packages have complex structures that need full collection
packages_to_collect = [
    'webview',      # pywebview with all platforms
    'aiohttp',      # Async HTTP
    'esptool',      # ESP32 flasher
    'serial',       # pyserial
    'clr_loader',   # .NET loader
    'pyright',      # Language server
]

for package in packages_to_collect:
    try:
        tmp_ret = collect_all(package)
        datas += tmp_ret[0]
        binaries += tmp_ret[1]
        hiddenimports += tmp_ret[2]
    except Exception as e:
        print(f"Warning: Could not collect {package}: {e}")

# =============================================================================
# ANALYSIS
# =============================================================================

a = Analysis(
    # Entry point
    [os.path.join(SRC_DIR, 'main.py')],

    # Additional paths to search for imports
    pathex=[SRC_DIR],

    # Binary dependencies
    binaries=binaries,

    # Data files to include
    datas=datas,

    # Hidden imports
    hiddenimports=hiddenimports,

    # Custom hooks path
    hookspath=[],

    # Hook configuration
    hooksconfig={},

    # Runtime hooks
    runtime_hooks=[],

    # Modules to exclude
    excludes=[
        # Exclude test frameworks
        'pytest',
        'unittest',
        '_pytest',

        # Exclude unused GUI frameworks
        'tkinter',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',

        # Exclude development tools
        'IPython',
        'jupyter',
        'notebook',

        # Exclude unused webview platforms
        'webview.platforms.android',
        'webview.platforms.cocoa',
        'webview.platforms.gtk',
        'webview.platforms.qt',
    ],

    # Don't use archive for faster startup
    noarchive=False,

    # Optimization level
    optimize=0,
)

# =============================================================================
# PYZ ARCHIVE
# =============================================================================

pyz = PYZ(
    a.pure,
    a.zipped_data,
)

# =============================================================================
# EXECUTABLE
# =============================================================================

# Icon path
icon_path = os.path.join(ASSETS_DIR, 'icon.ico')
icon_arg = icon_path if os.path.exists(icon_path) else None

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],

    # Application name
    name='Pulsar',

    # Debug mode (set to True for troubleshooting)
    debug=False,

    # Bootloader settings
    bootloader_ignore_signals=False,

    # Strip debug symbols (reduces size)
    strip=False,

    # UPX compression (reduces size but may cause issues)
    upx=True,
    upx_exclude=[],

    # Runtime temp directory
    runtime_tmpdir=None,

    # Console window (False = windowed application)
    console=False,

    # Disable traceback window
    disable_windowed_traceback=False,

    # macOS specific
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,

    # Application icon
    icon=icon_arg,

    # Version info (Windows only)
    version=None,  # Can be set to 'version_info.txt' for detailed version
)

# =============================================================================
# BUILD NOTES
# =============================================================================
"""
Post-build checklist:

1. Test the executable:
   - Run Pulsar.exe
   - Connect an ESP32 device
   - Test REPL communication
   - Test file browser
   - Test code editor with autocompletion

2. Check file size:
   - Expected: 45-55 MB
   - If larger, check for unnecessary dependencies

3. Troubleshooting:
   - If app crashes, rebuild with console=True for error messages
   - Check build/Pulsar/warn-Pulsar.txt for warnings
   - Check xref-Pulsar.html for dependency graph

4. Distribution:
   - The single Pulsar.exe contains everything
   - No installation required
   - Works on Windows 10/11 x64
"""
