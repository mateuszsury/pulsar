<p align="center">
  <img src="assets/logo.png" alt="Pulsar Logo" width="120" height="120">
</p>

<h1 align="center">Pulsar</h1>

<p align="center">
  <strong>Signal Your Code to Life</strong>
</p>

<p align="center">
  Professional Desktop IDE for ESP32 & MicroPython Development
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#mcp-integration">MCP Integration</a> •
  <a href="#license">License</a>
</p>

---

## Overview

**Pulsar** is a modern, feature-rich desktop IDE designed specifically for ESP32 and MicroPython development. It provides a seamless development experience with real-time device communication, intelligent code completion, and integrated tools for firmware management.

Built with a React frontend and Python backend, Pulsar offers a VS Code-like interface optimized for embedded development workflows.

## Features

### Core Features

- **Multi-Device Management** - Connect and manage multiple ESP32 devices simultaneously
- **Interactive REPL Terminal** - Full-featured Python REPL with xterm.js terminal emulation
- **Monaco Code Editor** - Professional code editor with syntax highlighting and IntelliSense
- **File Browser** - Browse, upload, download, and manage files on your ESP32
- **Real-time Communication** - WebSocket-based real-time device output streaming

### Development Tools

- **LSP Support** - Full Language Server Protocol support via Pyright
- **50+ MicroPython Stubs** - Comprehensive type stubs for intelligent autocompletion
- **Firmware Flasher** - Built-in esptool integration for flashing MicroPython firmware
- **WiFi Manager** - Configure and manage WiFi connections on ESP32
- **Library Manager** - Install packages from micropython-lib, PyPI, and GitHub

### Advanced Features

- **MCP Integration** - Claude Desktop integration for AI-assisted development
- **Command History** - Navigate through command history with Up/Down arrows
- **Scroll Lock** - Lock terminal scrolling to review output
- **Log Export** - Export terminal sessions as JSON for debugging
- **Soft/Hard Reset** - Reset devices directly from the IDE

## Screenshots

<p align="center">
  <img src="assets/screenshot-main.png" alt="Main Interface" width="800">
  <br>
  <em>Main IDE Interface with Code Editor and Terminal</em>
</p>

<p align="center">
  <img src="assets/screenshot-files.png" alt="File Browser" width="800">
  <br>
  <em>File Browser with ESP32 Filesystem</em>
</p>

## Installation

### Option 1: Download Pre-built Executable (Recommended)

Download the latest `Pulsar.exe` from the [Releases](https://github.com/your-repo/pulsar/releases) page.

No installation required - just run the executable.

### Option 2: Build from Source

#### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Git

#### Steps

```bash
# Clone the repository
git clone https://github.com/your-repo/pulsar.git
cd pulsar

# Install Python dependencies
pip install -e ".[dev]"

# Install frontend dependencies
cd frontend && npm install && cd ..

# Run in development mode
python -m pulsar --dev
```

#### Building the Executable

```bash
# Install build dependencies
pip install -e ".[build]"

# Build the application
python build_pyinstaller.py
```

The built executable will be available at `dist/dist/Pulsar.exe`.

## Usage

### Quick Start

1. **Launch Pulsar** - Run `Pulsar.exe` or `python -m pulsar`
2. **Connect Device** - Connect your ESP32 via USB
3. **Select Port** - Click on the detected COM port in the sidebar
4. **Start Coding** - Use the REPL or create files in the editor

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Interrupt running code |
| `Ctrl+L` | Clear terminal |
| `Ctrl+R` | Soft reset device |
| `Ctrl+Shift+R` | Hard reset device |
| `Ctrl+S` | Save/Export logs |
| `Ctrl+D` | Disconnect device |
| `Ctrl+V` | Paste (with multi-line confirmation) |
| `Up/Down` | Navigate command history |
| `Escape` | Cancel current input |

### Command Line Options

```bash
pulsar [OPTIONS]

Options:
  --dev         Run in development mode (uses Vite dev server)
  --debug       Enable debug logging
  --port PORT   HTTP server port (default: 8765)
  --no-window   Run without GUI (API server only)
```

## Architecture

```
Pulsar/
├── src/                          # Python Backend
│   ├── main.py                   # Application entry point
│   ├── core/                     # Core modules
│   │   ├── app.py               # Main application class
│   │   ├── config.py            # Configuration management
│   │   └── events.py            # Event bus system
│   ├── server/                   # HTTP/WebSocket Server
│   │   ├── api.py               # REST API endpoints
│   │   └── websocket.py         # WebSocket handlers
│   ├── serial_manager/           # Serial Communication
│   │   ├── manager.py           # Device manager
│   │   ├── device.py            # Device abstraction
│   │   ├── repl.py              # REPL handler
│   │   └── file_transfer.py     # File operations
│   ├── tools/                    # Development Tools
│   │   ├── flasher.py           # Firmware flasher
│   │   ├── wifi.py              # WiFi manager
│   │   ├── sync.py              # Folder sync
│   │   └── lib_manager.py       # Library manager
│   ├── lsp/                      # Language Server Protocol
│   │   ├── manager.py           # LSP manager
│   │   └── protocol.py          # JSON-RPC protocol
│   ├── mcp_impl/                 # MCP Integration
│   │   ├── server.py            # MCP server
│   │   └── tools.py             # MCP tools
│   └── ui/                       # UI Layer
│       ├── window.py            # pywebview window
│       └── static/              # Built frontend files
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── App.tsx              # Main application component
│   │   ├── components/          # UI Components
│   │   │   ├── layout/          # Header, Sidebar, TabBar
│   │   │   ├── editor/          # Monaco Editor integration
│   │   │   ├── console/         # Terminal component
│   │   │   ├── files/           # File browser
│   │   │   └── tools/           # Tool panels
│   │   ├── stores/              # Zustand state management
│   │   ├── services/            # API clients
│   │   └── hooks/               # Custom React hooks
│   └── index.html               # HTML template
│
├── stubs/                        # MicroPython Type Stubs
│   ├── pyrightconfig.json       # Pyright configuration
│   └── micropython/             # 50+ stub files
│       ├── machine.pyi          # Hardware abstraction
│       ├── network.pyi          # WiFi/Ethernet
│       ├── bluetooth.pyi        # BLE support
│       ├── espnow.pyi           # ESP-NOW protocol
│       └── ...                  # And many more
│
└── assets/                       # Application assets
    ├── icon.ico                 # Application icon
    └── logo.png                 # Logo image
```

## MicroPython Type Stubs

Pulsar includes comprehensive type stubs for intelligent autocompletion:

### Built-in Modules (26)

| Category | Modules |
|----------|---------|
| **Hardware** | `machine`, `esp32`, `esp`, `bluetooth`, `espnow`, `neopixel` |
| **Sensors** | `dht`, `onewire`, `ds18x20` |
| **Display** | `framebuf` |
| **Network** | `network`, `usocket`, `ntptime` |
| **Async** | `uasyncio`, `uselect` |
| **Data** | `ujson`, `ustruct`, `ubinascii`, `ure` |
| **Crypto** | `uhashlib`, `ucryptolib` |
| **Utility** | `uos`, `utime`, `uio`, `ucollections`, `urandom`, `ulogging`, `gc`, `micropython` |

### External Libraries (24)

| Category | Libraries |
|----------|-----------|
| **MQTT** | `umqtt.simple`, `umqtt.robust` |
| **HTTP/Web** | `urequests`, `microdot`, `uwebsocket` |
| **Displays** | `ssd1306`, `sh1106` (OLED), `st7789`, `ili9341` (LCD), `max7219` (LED) |
| **Sensors** | `bme280`, `mpu6050`, `ahtx0`, `hcsr04` |
| **RTC/ADC** | `ds3231`, `ads1115` |
| **Motor Control** | `pca9685`, `stepper` |
| **Storage** | `sdcard` |

## MCP Integration

Pulsar can be used with Claude Desktop for AI-assisted MicroPython development.

### Configuration

Add to your `claude_desktop_config.json`:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pulsar": {
      "command": "python",
      "args": ["-m", "mcp_impl.server"],
      "cwd": "C:/path/to/pulsar/src",
      "env": {
        "PYTHONPATH": "C:/path/to/pulsar/src"
      }
    }
  }
}
```

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `list_ports` | List available serial ports |
| `connect` | Connect to a device |
| `disconnect` | Disconnect from a device |
| `execute` | Execute Python code on device |
| `list_files` | List files on device |
| `read_file` | Read file contents |
| `write_file` | Write file to device |
| `delete_file` | Delete file from device |
| `reset` | Reset the device |

## API Reference

### REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/ports` | List available serial ports |
| `POST` | `/api/connect` | Connect to a device |
| `POST` | `/api/disconnect` | Disconnect from a device |
| `POST` | `/api/execute` | Execute code on device |
| `GET` | `/api/files` | List files on device |
| `GET` | `/api/file` | Read file content |
| `POST` | `/api/file` | Write file to device |
| `DELETE` | `/api/file` | Delete file from device |
| `POST` | `/api/reset` | Reset device |
| `POST` | `/api/flash` | Flash firmware |
| `GET` | `/api/wifi/scan` | Scan WiFi networks |
| `POST` | `/api/wifi/connect` | Connect to WiFi |

### WebSocket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `subscribe` | Client → Server | Subscribe to device output |
| `input` | Client → Server | Send input to device |
| `output` | Server → Client | Device output data |
| `connected` | Server → Client | Device connected |
| `disconnected` | Server → Client | Device disconnected |

## Configuration

Pulsar stores configuration in `~/.pulsar/config.json`:

```json
{
  "default_baudrate": 115200,
  "window_width": 1400,
  "window_height": 900
}
```

## Troubleshooting

### Device Not Detected

1. Ensure USB drivers are installed (CP210x or CH340)
2. Check Device Manager for COM port
3. Try a different USB cable (data cable, not charging-only)

### Connection Failed

1. Close other applications using the COM port
2. Try a lower baud rate (9600)
3. Reset the ESP32 and try again

### Firmware Flash Failed

1. Hold BOOT button while connecting
2. Use the correct firmware for your ESP32 variant
3. Try erasing flash first

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Tech Stack

- **Backend:** Python 3.11+, aiohttp, pyserial, pywebview
- **Frontend:** React 18, TypeScript, Tailwind CSS, Zustand
- **Editor:** Monaco Editor
- **Terminal:** xterm.js
- **LSP:** Pyright
- **Build:** PyInstaller, Vite

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Mateusz Sury**

---

<p align="center">
  Made with ❤️ for the ESP32 & MicroPython community
</p>
