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
  <a href="#why-pulsar">Why Pulsar?</a> •
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#tools">Tools</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Windows-blue" alt="Platform">
  <img src="https://img.shields.io/badge/python-3.11+-green" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange" alt="License">
  <img src="https://img.shields.io/badge/ESP32-MicroPython-red" alt="ESP32">
</p>

---

## Why Pulsar?

**Pulsar** was created to solve the frustrations of ESP32 MicroPython development. Unlike generic Python IDEs or basic serial monitors, Pulsar is built from the ground up specifically for embedded development.

### The Problem

- **Thonny** is great for beginners but lacks advanced features
- **VS Code** requires complex setup with multiple extensions
- **Arduino IDE** doesn't support MicroPython
- **Generic serial monitors** don't understand Python syntax

### The Solution

Pulsar combines everything you need in one lightweight, portable application:

| Feature | Pulsar | Thonny | VS Code | Serial Monitor |
|---------|--------|--------|---------|----------------|
| MicroPython Autocompletion | ✅ 50+ modules | ⚠️ Basic | ⚠️ Requires setup | ❌ |
| Multi-device Support | ✅ Unlimited | ❌ Single | ⚠️ Complex | ❌ |
| Firmware Flashing | ✅ Built-in | ✅ | ❌ External tool | ❌ |
| Folder Sync | ✅ One-click | ❌ | ❌ | ❌ |
| WiFi Configuration | ✅ Visual UI | ❌ | ❌ | ❌ |
| Library Manager | ✅ 3 sources | ⚠️ Basic | ❌ | ❌ |
| Portable | ✅ Single .exe | ❌ | ❌ | ✅ |

---

## Features

### 🖥️ Professional Code Editor

Pulsar uses **Monaco Editor** - the same editor that powers VS Code - providing a familiar, professional coding experience.

- **Syntax Highlighting** - Full Python/MicroPython syntax highlighting
- **Intelligent Autocompletion** - Context-aware suggestions as you type
- **Error Detection** - Real-time syntax error highlighting via Pyright LSP
- **Code Folding** - Collapse functions and classes for better overview
- **Multiple Tabs** - Work on multiple files simultaneously
- **Find & Replace** - Search across your code with regex support

### 🧠 50+ MicroPython Type Stubs

Get intelligent autocompletion for all MicroPython modules - no more guessing function signatures!

```python
from machine import Pin, I2C
from network import WLAN

# Pulsar knows all methods and parameters!
pin = Pin(2, Pin.OUT)  # Autocomplete shows: Pin.IN, Pin.OUT, Pin.PULL_UP...
wlan = WLAN(STA_IF)    # Autocomplete shows: scan(), connect(), isconnected()...
```

**Supported Modules:**

| Category | Modules |
|----------|---------|
| **Hardware** | `machine` (Pin, I2C, SPI, UART, PWM, ADC, Timer, RTC), `esp32`, `esp`, `neopixel` |
| **Networking** | `network`, `usocket`, `urequests`, `umqtt.simple`, `umqtt.robust`, `uwebsocket` |
| **Wireless** | `bluetooth` (BLE), `espnow` (ESP-NOW protocol) |
| **Displays** | `ssd1306`, `sh1106` (OLED), `st7789`, `ili9341` (LCD), `max7219` (LED matrix), `framebuf` |
| **Sensors** | `dht`, `ds18x20`, `onewire`, `bme280`, `mpu6050`, `ahtx0`, `hcsr04`, `ads1115` |
| **Motor/Servo** | `pca9685` (16-channel PWM), `stepper` |
| **Storage** | `sdcard`, `uos`, `ujson` |
| **Time** | `utime`, `ntptime`, `ds3231` (RTC) |
| **Async** | `uasyncio`, `uselect` |
| **Web Framework** | `microdot` (async web server) |
| **Crypto** | `uhashlib`, `ucryptolib`, `ubinascii` |

### 💻 Interactive REPL Terminal

Full-featured Python REPL with professional terminal emulation.

- **xterm.js Terminal** - True terminal experience with ANSI color support
- **Command History** - Navigate previous commands with Up/Down arrows
- **Multi-line Input** - Paste and execute multi-line code blocks
- **Scroll Lock** - Pause scrolling to review output
- **Log Export** - Save terminal sessions as JSON for debugging
- **Keyboard Shortcuts** - `Ctrl+C` interrupt, `Ctrl+L` clear, `Ctrl+R` reset

### 📁 File Browser & Manager

Complete filesystem management for your ESP32.

- **Visual Tree View** - Browse files and folders on your device
- **Drag & Drop Upload** - Simply drag files to upload them
- **Download Files** - Save device files to your computer
- **Create/Delete** - Manage files and folders directly
- **File Preview** - View file contents before editing
- **Context Menu** - Right-click for quick actions

### 🔄 Folder Synchronization

**One-click project deployment** - the killer feature for serious development!

Instead of uploading files one by one, Pulsar can synchronize an entire folder from your computer to ESP32:

1. **Select local folder** - Choose your project directory
2. **Click Sync** - Pulsar compares files and uploads only changes
3. **Done!** - Your entire project is on the device

**Smart Sync Features:**
- **Incremental Upload** - Only changed files are transferred
- **Delete Orphans** - Remove files from device that don't exist locally
- **Exclude Patterns** - Skip `__pycache__`, `.git`, etc.
- **Progress Tracking** - See which files are being transferred
- **Conflict Detection** - Warning when device files are newer

**Perfect for:**
- Projects with multiple modules
- Rapid iteration during development
- Deploying production code
- Team collaboration (sync from Git repo)

### ⚡ Firmware Flasher

Flash MicroPython firmware without leaving the IDE.

- **Auto-detect Chip** - Recognizes ESP32, ESP32-C3, ESP32-S3, ESP32-C6
- **Download Firmware** - Get latest MicroPython directly from micropython.org
- **Erase Flash** - Clean slate before flashing
- **Progress Tracking** - Real-time flash progress
- **Verify** - Confirm successful flash

**Supported chips:**
- ESP32 (WROOM, WROVER)
- ESP32-C3
- ESP32-C6
- ESP32-S2
- ESP32-S3
- ESP8266

### 📶 WiFi Manager

Configure ESP32 WiFi visually - no more typing credentials in REPL!

- **Scan Networks** - See all available WiFi networks
- **Signal Strength** - Visual indicator of network quality
- **Connect** - One-click connection with password input
- **Save Credentials** - Store networks for auto-connect
- **AP Mode** - Configure Access Point settings
- **Status Display** - Current IP address, connection status

### 📦 Library Manager

Install MicroPython packages from multiple sources.

**Sources:**
1. **micropython-lib** - Official MicroPython packages
2. **PyPI** - Python Package Index (MicroPython-compatible)
3. **GitHub** - Install directly from repositories

**Features:**
- **Search** - Find packages by name or description
- **One-click Install** - Download and upload to device
- **Dependencies** - Automatic dependency resolution
- **Version Selection** - Choose specific versions
- **Uninstall** - Remove packages cleanly

### 🔌 Multi-Device Support

Work with multiple ESP32 devices simultaneously!

- **Device List** - See all connected devices
- **Quick Switch** - Click to change active device
- **Parallel Terminals** - Open REPL for each device
- **Device Info** - Chip type, MAC address, flash size
- **Color Coding** - Distinguish devices visually

**Use cases:**
- Master-slave communication testing
- Mesh network development
- Production line programming
- Comparative debugging

### 🤖 AI-Assisted Development (MCP Integration)

Pulsar integrates with **Claude Desktop** through the **Model Context Protocol (MCP)**, enabling revolutionary AI-powered ESP32 development. Claude becomes your intelligent coding partner with direct access to your hardware!

---

## MCP Integration Guide

### What is MCP?

**Model Context Protocol (MCP)** is Anthropic's open standard that allows AI assistants like Claude to interact with external tools and services. With Pulsar's MCP integration, Claude can:

- 🔌 **Connect to your ESP32** - Establish serial connections
- ▶️ **Execute code directly** - Run Python on your device in real-time
- 📁 **Manage files** - Read, write, and delete files on ESP32
- 🔍 **Debug interactively** - Test code and see results immediately
- 🛠️ **Flash firmware** - Update MicroPython on your device
- 📶 **Configure WiFi** - Set up network connections

### Setup Instructions

#### Step 1: Install Claude Desktop

Download Claude Desktop from [claude.ai/download](https://claude.ai/download) if you haven't already.

#### Step 2: Configure MCP Server

Open your Claude Desktop configuration file:

| OS | Path |
|----|------|
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

Add the Pulsar MCP server configuration:

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

> **Note:** Replace `C:/path/to/pulsar` with your actual Pulsar installation path.

#### Step 3: Restart Claude Desktop

Close and reopen Claude Desktop. You should see the Pulsar tools available in Claude's tool list.

### Available MCP Tools

| Tool | Description | Example Use |
|------|-------------|-------------|
| `list_ports` | List all available serial ports | "What ESP32 devices are connected?" |
| `connect` | Connect to a device by port | "Connect to COM4" |
| `disconnect` | Disconnect from current device | "Disconnect from the ESP32" |
| `execute` | Run Python code on device | "Turn on the LED on pin 2" |
| `list_files` | List files on device filesystem | "What files are on my ESP32?" |
| `read_file` | Read file contents from device | "Show me the contents of main.py" |
| `write_file` | Write/create file on device | "Create a boot.py that connects to WiFi" |
| `delete_file` | Delete file from device | "Remove the old config.json" |
| `reset` | Reset the device (soft/hard) | "Reset the ESP32" |
| `get_device_info` | Get chip info, MAC, flash size | "What ESP32 model is this?" |

### Example Conversations with Claude

#### Example 1: Quick LED Test

**You:** "Connect to my ESP32 on COM4 and blink the onboard LED"

**Claude:** *Uses `connect` tool, then `execute` tool*
```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)
for i in range(5):
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)
```
"Done! The LED should have blinked 5 times."

---

#### Example 2: Create IoT Sensor Project

**You:** "Create a temperature monitoring system that reads from DHT22 on pin 4 and sends data to my MQTT broker at 192.168.1.100"

**Claude:** *Creates multiple files using `write_file` tool*

```python
# config.py
WIFI_SSID = "YourNetwork"
WIFI_PASSWORD = "YourPassword"
MQTT_BROKER = "192.168.1.100"
MQTT_TOPIC = "home/temperature"
DHT_PIN = 4
INTERVAL = 60  # seconds
```

```python
# main.py
from machine import Pin
from dht import DHT22
from umqtt.simple import MQTTClient
import network
import time
import config

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

while not wlan.isconnected():
    time.sleep(1)

print(f"Connected: {wlan.ifconfig()[0]}")

# Setup sensor and MQTT
sensor = DHT22(Pin(config.DHT_PIN))
client = MQTTClient("esp32_temp", config.MQTT_BROKER)
client.connect()

# Main loop
while True:
    sensor.measure()
    temp = sensor.temperature()
    humidity = sensor.humidity()

    payload = f'{{"temp": {temp}, "humidity": {humidity}}}'
    client.publish(config.MQTT_TOPIC, payload)
    print(f"Sent: {payload}")

    time.sleep(config.INTERVAL)
```

"I've created the project files. Want me to upload them and test?"

---

#### Example 3: Debug a Problem

**You:** "My ESP32 keeps crashing when I try to connect to WiFi. Here's my code..."

**Claude:** *Uses `execute` tool to test incrementally*

"Let me test the WiFi connection step by step on your device..."

```python
import network
wlan = network.WLAN(network.STA_IF)
print(f"Interface active: {wlan.active()}")
```

"The interface is inactive. Let me activate it and check for errors..."

```python
wlan.active(True)
print(f"Active: {wlan.active()}")
print(f"Scan results: {wlan.scan()}")
```

"Found the issue! Your network 'MyWiFi' uses WPA3 which isn't supported. Try connecting to a WPA2 network or update your router settings."

---

#### Example 4: File Management

**You:** "Show me all files on my ESP32 and clean up any .pyc files"

**Claude:** *Uses `list_files` and `delete_file` tools*

"Here's what's on your device:
- `/boot.py` (245 bytes)
- `/main.py` (1.2 KB)
- `/lib/` (directory)
- `/lib/umqtt.pyc` (892 bytes)
- `/config.pyc` (156 bytes)

I found 2 .pyc files. Deleting them now..."

"Done! Removed `umqtt.pyc` and `config.pyc`. These compiled files aren't needed on MicroPython."

---

#### Example 5: Hardware Discovery

**You:** "I just got a new ESP32 board. Tell me everything about it."

**Claude:** *Uses `connect` and `get_device_info` tools, then `execute`*

"Connected! Here's your board info:

| Property | Value |
|----------|-------|
| **Chip** | ESP32-S3 |
| **Flash** | 8MB |
| **PSRAM** | 2MB |
| **MAC** | `AA:BB:CC:DD:EE:FF` |
| **MicroPython** | v1.23.0 |

Let me also check the pins..."

```python
import machine
print(f"CPU Freq: {machine.freq()/1e6} MHz")
print(f"Free memory: {gc.mem_free()} bytes")
```

"Your ESP32-S3 is running at 240 MHz with 142KB free RAM. It has native USB support - perfect for fast development!"

---

### Tips for Using Claude with Pulsar

#### 1. Be Specific About Hardware

```
❌ "Make an LED blink"
✅ "Blink the LED connected to GPIO 2 on my ESP32"
```

#### 2. Mention Your Sensor Models

```
❌ "Read the temperature"
✅ "Read temperature from DHT22 sensor on pin 4"
```

#### 3. Provide Context

```
❌ "Fix my code"
✅ "My code crashes after 10 minutes. I suspect a memory leak. Here's main.py..."
```

#### 4. Ask for Step-by-Step Testing

```
"Test each part of this code separately to find where it fails"
```

#### 5. Request Explanations

```
"Write code to control a servo, and explain each line"
```

### Workflow: AI-Powered Development Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT CYCLE                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DESCRIBE          "I want to build a smart doorbell     │
│     ────────►          with camera and MQTT notifications"  │
│                                                             │
│  2. CLAUDE DESIGNS    Creates project structure, suggests   │
│     ────────►         components, writes initial code       │
│                                                             │
│  3. DEPLOY            Claude uploads files to ESP32         │
│     ────────►         using write_file tool                 │
│                                                             │
│  4. TEST              Claude executes code, checks output   │
│     ────────►         using execute tool                    │
│                                                             │
│  5. DEBUG             If errors, Claude reads logs,         │
│     ────────►         modifies code, retests                │
│                                                             │
│  6. ITERATE           Refine until working perfectly        │
│     ────────►                                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Security Considerations

- **Local Only** - MCP runs locally, no cloud connection required
- **No Auto-Execute** - Claude asks before running code on your device
- **Full Visibility** - All commands are shown in Claude's responses
- **You Control Access** - Only you can approve tool usage

---

## Installation

### Option 1: Download Executable (Recommended)

1. Download `Pulsar-v0.1.0-windows-x64.zip` from [Releases](https://github.com/mateuszsury/pulsar/releases)
2. Extract `Pulsar.exe`
3. Run - no installation required!

**Requirements:**
- Windows 10/11 (x64)
- USB drivers for your ESP32 (CP210x or CH340)

### Option 2: Build from Source

```bash
# Clone repository
git clone https://github.com/mateuszsury/pulsar.git
cd pulsar

# Install Python dependencies
pip install -e ".[dev]"

# Install frontend dependencies
cd frontend && npm install && cd ..

# Run in development mode
python -m pulsar --dev
```

**Build executable:**
```bash
pip install -e ".[build]"
python build_pyinstaller.py
```

---

## Getting Started

### 1. Connect Your ESP32

1. Connect ESP32 to your computer via USB
2. Launch Pulsar
3. Your device appears in the sidebar automatically

### 2. Flash MicroPython (if needed)

If your ESP32 doesn't have MicroPython:

1. Go to **Tools → Firmware Flasher**
2. Select your chip type
3. Click **Download & Flash**
4. Wait for completion

### 3. Start Coding!

**Quick REPL test:**
```python
>>> from machine import Pin
>>> led = Pin(2, Pin.OUT)
>>> led.value(1)  # LED on!
```

**Create a project:**
1. Create files in the editor
2. Use **Folder Sync** to upload your project
3. Run with `import main` in REPL

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Interrupt running code |
| `Ctrl+L` | Clear terminal |
| `Ctrl+R` | Soft reset device |
| `Ctrl+Shift+R` | Hard reset device |
| `Ctrl+S` | Save current file / Export logs |
| `Ctrl+D` | Disconnect device |
| `Up/Down` | Navigate command history |
| `Escape` | Cancel current input |

---

## Use Cases

### IoT Sensor Node

```python
from machine import Pin, I2C
from bme280 import BME280
import urequests
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
sensor = BME280(i2c=i2c)

while True:
    temp, pressure, humidity = sensor.values
    urequests.post("http://server/data", json={
        "temperature": temp,
        "humidity": humidity
    })
    time.sleep(60)
```

### LED Controller

```python
from machine import Pin
from neopixel import NeoPixel
import network

np = NeoPixel(Pin(5), 30)
wlan = network.WLAN(network.STA_IF)

# Pulsar's autocompletion helps with all NeoPixel methods!
np[0] = (255, 0, 0)  # Red
np.write()
```

### MQTT Smart Home

```python
from umqtt.simple import MQTTClient
from machine import Pin

client = MQTTClient("esp32", "mqtt.server.com")
relay = Pin(4, Pin.OUT)

def callback(topic, msg):
    if msg == b"on":
        relay.value(1)
    else:
        relay.value(0)

client.set_callback(callback)
client.connect()
client.subscribe(b"home/relay")
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.11+, aiohttp, pyserial-asyncio, pywebview |
| **Frontend** | React 18, TypeScript, Tailwind CSS, Zustand |
| **Editor** | Monaco Editor |
| **Terminal** | xterm.js |
| **LSP** | Pyright |
| **Flash Tool** | esptool |
| **Build** | PyInstaller, Vite |

---

## Troubleshooting

### Device Not Detected

1. **Install USB drivers** - CP210x for most ESP32 boards, CH340 for cheap clones
2. **Check cable** - Use a data cable, not charge-only
3. **Try different port** - Some USB ports have issues

### Connection Failed

1. **Close other apps** - Ensure no other program uses the COM port
2. **Reset device** - Press EN/RST button on ESP32
3. **Lower baud rate** - Try 9600 if 115200 fails

### Flash Failed

1. **Enter boot mode** - Hold BOOT button while pressing EN
2. **Correct firmware** - Match firmware to your exact chip variant
3. **Erase first** - Try erasing flash before flashing

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

**Mateusz Sury**

---

<p align="center">
  <strong>Pulsar</strong> - The IDE that speaks MicroPython
</p>

<p align="center">
  Built for the ESP32 & MicroPython community
</p>
