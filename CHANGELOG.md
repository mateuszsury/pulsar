# Changelog

All notable changes to Pulsar will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-04

### Added

- **Core IDE Features**
  - Multi-device management for simultaneous ESP32 connections
  - Interactive REPL terminal with xterm.js emulation
  - Monaco code editor with Python syntax highlighting
  - File browser for ESP32 filesystem management
  - Real-time WebSocket communication with devices

- **Development Tools**
  - Firmware flasher with esptool integration
  - WiFi manager for ESP32 network configuration
  - Library manager supporting micropython-lib, PyPI, and GitHub
  - Folder synchronization tool

- **LSP Support**
  - Full Pyright integration for intelligent autocompletion
  - 50+ MicroPython type stubs including:
    - Built-in modules: `machine`, `network`, `esp32`, `bluetooth`, `espnow`, etc.
    - External libraries: `umqtt`, `urequests`, `ssd1306`, `bme280`, etc.

- **MCP Integration**
  - Claude Desktop integration for AI-assisted development
  - MCP tools for device management and code execution

- **User Interface**
  - VS Code-like dark theme interface
  - Keyboard shortcuts for common operations
  - Command history navigation
  - Scroll lock for terminal output
  - Log export functionality

### Technical Details

- Python 3.11+ backend with aiohttp and pywebview
- React 18 frontend with TypeScript and Tailwind CSS
- PyInstaller packaging for single-file Windows executable

---

## Roadmap

### [0.2.0] - Planned

- [ ] Syntax highlighting for MicroPython-specific constructs
- [ ] Integrated debugger support
- [ ] Project templates for common ESP32 applications
- [ ] OTA firmware update support
- [ ] Multiple workspace support

### [0.3.0] - Planned

- [ ] macOS support
- [ ] Linux support
- [ ] Plugin system for extensibility
- [ ] Integrated serial monitor with filtering
- [ ] Memory profiler for ESP32

### Future

- [ ] Cloud sync for projects
- [ ] Collaborative editing
- [ ] ESP-IDF integration
- [ ] Circuit diagram viewer
