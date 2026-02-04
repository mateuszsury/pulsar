# ThonnyV2 MCP Integration Guide

This document describes how to integrate ThonnyV2 with Claude Desktop using the Model Context Protocol (MCP).

## Quick Start

### 1. Generate Configuration

Run the config generator:

```bash
cd ThonnyV2/src
python -m mcp_impl.config_generator
```

This will output the JSON configuration to add to your `claude_desktop_config.json`.

### 2. Configuration File Locations

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 3. Example Configuration

```json
{
  "mcpServers": {
    "thonnyv2": {
      "command": "python",
      "args": ["-m", "mcp_impl.server"],
      "cwd": "/path/to/ThonnyV2/src",
      "env": {
        "PYTHONPATH": "/path/to/ThonnyV2/src"
      }
    }
  }
}
```

### 4. Restart Claude Desktop

After adding the configuration, restart Claude Desktop to load the MCP server.

---

## Available Tools

### Port & Connection Tools

#### `list_ports`
List all available serial ports on the system.

```
No parameters required.
```

#### `list_esp32_ports`
List only ESP32 devices (filters by known USB chip VIDs).

```
No parameters required.
```

#### `connect`
Connect to a MicroPython device on the specified port.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| port | string | Yes | - | Serial port (e.g., COM4, /dev/ttyUSB0) |
| baudrate | integer | No | 115200 | Baud rate |

Example:
```
connect COM4
connect /dev/ttyUSB0 115200
```

#### `disconnect`
Disconnect from a device.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| port | string | Yes | Serial port |

#### `list_devices`
List all currently connected devices.

```
No parameters required.
```

#### `get_device_info`
Get detailed information about a connected device.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| port | string | Yes | Serial port |

---

### REPL & Execution Tools

#### `execute`
Execute Python code on a MicroPython device.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| port | string | Yes | - | Serial port |
| code | string | Yes | - | Python code to execute |
| timeout | number | No | 30.0 | Execution timeout in seconds |

Example:
```
execute COM4 "print('Hello from ESP32!')"
execute COM4 "import machine; led = machine.Pin(2, machine.Pin.OUT); led.on()"
```

#### `interrupt`
Send Ctrl+C to interrupt running code on a device.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| port | string | Yes | Serial port |

#### `reset`
Reset the MicroPython device.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| port | string | Yes | - | Serial port |
| soft | boolean | No | true | Soft reset (true) or hard reset (false) |

---

### File Operations

#### `list_files`
List files and directories on the device.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| port | string | Yes | - | Serial port |
| path | string | No | "/" | Directory path |

#### `read_file`
Read a file from the device.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| port | string | Yes | Serial port |
| path | string | Yes | File path on device |

Returns:
- `content`: File content (text or base64 for binary)
- `binary`: Whether content is base64-encoded
- `size`: File size in bytes

#### `write_file`
Write a file to the device.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| port | string | Yes | - | Serial port |
| path | string | Yes | - | File path on device |
| content | string | Yes | - | File content |
| binary | boolean | No | false | Is content base64-encoded? |

#### `delete_file`
Delete a file from the device.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| port | string | Yes | Serial port |
| path | string | Yes | File path |

#### `mkdir`
Create a directory on the device.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| port | string | Yes | Serial port |
| path | string | Yes | Directory path to create |

#### `upload_file`
Upload a local file to the device.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| port | string | Yes | Serial port |
| local_path | string | Yes | Path to local file |
| remote_path | string | Yes | Destination path on device |

Example:
```
upload_file COM4 ./main.py /main.py
```

#### `download_file`
Download a file from the device to local filesystem.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| port | string | Yes | Serial port |
| remote_path | string | Yes | File path on device |
| local_path | string | Yes | Destination path locally |

---

### Monitoring & Logging

#### `get_logs`
Get recent output logs from a device.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| port | string | Yes | - | Serial port |
| limit | integer | No | 100 | Maximum number of lines |

#### `watch_logs`
Watch device output for a specified duration (useful for monitoring real-time events).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| port | string | Yes | - | Serial port |
| duration | integer | No | 30 | Watch duration in seconds |
| filter_pattern | string | No | "" | Regex pattern to filter output |

Example:
```
watch_logs COM4 60
watch_logs COM4 30 "error|warning"
```

---

### Device Information

#### `get_wifi_status`
Get WiFi connection status including IP address, RSSI, and AP info.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| port | string | Yes | Serial port |

Returns:
- `sta_active`: Station interface active
- `sta_connected`: Connected to WiFi
- `sta_config`: IP configuration (IP, netmask, gateway, DNS)
- `sta_rssi`: Signal strength (if available)
- `ap_active`: Access point interface active
- `ap_config`: AP IP configuration
- `ap_essid`: AP network name

#### `get_chip_info`
Get ESP chip information using esptool.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| port | string | Yes | Serial port |

Returns:
- `chip`: Chip type (e.g., ESP32-C6)
- `chip_id`: Chip ID
- `mac_address`: MAC address
- `flash_size`: Flash size
- `crystal`: Crystal frequency
- `features`: List of chip features

---

### Folder Sync

#### `sync_folder`
Sync a local folder to the device (only uploads changed files).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| port | string | Yes | - | Serial port |
| local_path | string | Yes | - | Local folder path |
| remote_path | string | No | "/" | Remote folder on device |
| dry_run | boolean | No | false | Only show what would be uploaded |

Example:
```
sync_folder COM4 ./src /
sync_folder COM4 ./project /app true  # dry run
```

---

## Usage Examples with Claude

### Upload and Run Code

```
Please upload main.py to my ESP32 on COM4 and run it
```

### Monitor Device

```
Watch logs on COM4 for 30 seconds and tell me if there are any errors
```

### Deploy Project

```
Sync my ./firmware folder to the ESP32 on COM4 and then reset the device
```

### Debug WiFi Issues

```
Check the WiFi status on COM4 and help me troubleshoot the connection
```

### Get Device Info

```
What type of ESP32 chip is connected to COM4? Get the full chip info.
```

---

## Troubleshooting

### MCP Server Not Loading

1. Check that Python is in your PATH
2. Verify the `cwd` path in config is correct
3. Check Claude Desktop logs for errors

### Connection Issues

1. Ensure ThonnyV2 GUI is not also connected (only one connection at a time)
2. Check that the device is properly connected via USB
3. Try a different baud rate (115200 is standard)

### Timeout Errors

1. Increase the `timeout` parameter for long-running operations
2. Check if the device is in a busy state
3. Try `interrupt` then retry the operation
