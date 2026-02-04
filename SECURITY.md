# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Pulsar, please report it responsibly.

### How to Report

**Email:** mateuszsury25@gmail.com

**Subject:** [SECURITY] Brief description of the vulnerability

### What to Include

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)

### Response Time

- **Acknowledgment:** Within 48 hours
- **Initial Assessment:** Within 7 days
- **Resolution Timeline:** Depends on severity

### What to Expect

1. We will acknowledge receipt of your report
2. We will investigate and validate the vulnerability
3. We will work on a fix
4. We will release a patch and credit you (if desired)

### Please Do Not

- Publicly disclose the vulnerability before it's fixed
- Exploit the vulnerability beyond what's necessary to demonstrate it
- Access or modify other users' data

## Security Best Practices for Users

### Serial Port Access

Pulsar requires access to serial ports to communicate with ESP32 devices. This is normal and expected behavior.

### MCP Integration

When using MCP with Claude Desktop:
- All code execution happens locally on your machine
- Claude can only access devices you explicitly connect
- You can review all commands before execution

### Firmware Flashing

Only flash firmware from trusted sources:
- Official MicroPython releases (micropython.org)
- Your own compiled firmware

## Contact

For security concerns: **mateuszsury25@gmail.com**
