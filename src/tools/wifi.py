"""WiFi configuration manager for MicroPython devices."""

import asyncio
import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from serial_comm.manager import SerialManager

logger = logging.getLogger(__name__)


@dataclass
class WiFiNetwork:
    """WiFi network information."""

    ssid: str
    bssid: str
    channel: int
    rssi: int
    authmode: int
    hidden: bool

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        auth_names = {
            0: "open",
            1: "WEP",
            2: "WPA-PSK",
            3: "WPA2-PSK",
            4: "WPA/WPA2-PSK",
        }
        return {
            "ssid": self.ssid,
            "bssid": self.bssid,
            "channel": self.channel,
            "rssi": self.rssi,
            "authmode": auth_names.get(self.authmode, f"unknown({self.authmode})"),
            "hidden": self.hidden,
            "signal": self._rssi_to_signal(),
        }

    def _rssi_to_signal(self) -> str:
        """Convert RSSI to signal quality."""
        if self.rssi >= -50:
            return "excellent"
        elif self.rssi >= -60:
            return "good"
        elif self.rssi >= -70:
            return "fair"
        else:
            return "weak"


@dataclass
class WiFiStatus:
    """WiFi connection status."""

    connected: bool
    ssid: str = ""
    ip: str = ""
    netmask: str = ""
    gateway: str = ""
    dns: str = ""
    mac: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "connected": self.connected,
            "ssid": self.ssid,
            "ip": self.ip,
            "netmask": self.netmask,
            "gateway": self.gateway,
            "dns": self.dns,
            "mac": self.mac,
        }


class WiFiManager:
    """Manages WiFi configuration on MicroPython devices."""

    def __init__(self, serial_manager: "SerialManager") -> None:
        self.serial_manager = serial_manager

    async def scan(self, port: str) -> list[dict]:
        """Scan for available WiFi networks."""
        code = """
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
networks = wlan.scan()
for n in networks:
    ssid, bssid, channel, rssi, authmode, hidden = n
    bssid_str = ':'.join(['%02x' % b for b in bssid])
    print(repr((ssid.decode('utf-8', 'replace'), bssid_str, channel, rssi, authmode, hidden)))
"""
        result = await self.serial_manager.execute(port, code)

        networks = []
        for line in result.output.strip().split("\n"):
            line = line.strip()
            if line and line.startswith("("):
                try:
                    data = eval(line)
                    networks.append(WiFiNetwork(
                        ssid=data[0],
                        bssid=data[1],
                        channel=data[2],
                        rssi=data[3],
                        authmode=data[4],
                        hidden=data[5],
                    ).to_dict())
                except Exception as e:
                    logger.warning("Failed to parse network: %s", e)

        # Sort by signal strength
        networks.sort(key=lambda n: n.get("rssi", -100), reverse=True)
        return networks

    async def configure(
        self,
        port: str,
        ssid: str,
        password: str = "",
        timeout: int = 15,
    ) -> bool:
        """Configure WiFi connection."""
        code = f"""
import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Disconnect if connected
if wlan.isconnected():
    wlan.disconnect()
    time.sleep(0.5)

# Connect
wlan.connect({repr(ssid)}, {repr(password)})

# Wait for connection
start = time.time()
while not wlan.isconnected():
    if time.time() - start > {timeout}:
        print('TIMEOUT')
        break
    time.sleep(0.5)

if wlan.isconnected():
    print('CONNECTED')
    config = wlan.ifconfig()
    print('IP:', config[0])
else:
    print('FAILED')
"""
        result = await self.serial_manager.execute(port, code, timeout=timeout + 5)

        return "CONNECTED" in result.output

    async def get_status(self, port: str) -> dict:
        """Get current WiFi status."""
        code = """
import network
import ubinascii

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

connected = wlan.isconnected()
config = wlan.ifconfig() if connected else ('', '', '', '')
mac = ubinascii.hexlify(wlan.config('mac'), ':').decode()

try:
    ssid = wlan.config('essid') if connected else ''
except:
    ssid = ''

print(repr({
    'connected': connected,
    'ssid': ssid,
    'ip': config[0],
    'netmask': config[1],
    'gateway': config[2],
    'dns': config[3],
    'mac': mac,
}))
"""
        result = await self.serial_manager.execute(port, code)

        try:
            # Find the dict in output
            for line in result.output.strip().split("\n"):
                if line.strip().startswith("{"):
                    data = eval(line.strip())
                    return WiFiStatus(**data).to_dict()
        except Exception as e:
            logger.warning("Failed to parse WiFi status: %s", e)

        return WiFiStatus(connected=False).to_dict()

    async def disconnect(self, port: str) -> bool:
        """Disconnect from WiFi."""
        code = """
import network
wlan = network.WLAN(network.STA_IF)
wlan.disconnect()
wlan.active(False)
print('OK')
"""
        result = await self.serial_manager.execute(port, code)
        return "OK" in result.output

    async def set_ap(
        self,
        port: str,
        ssid: str,
        password: str = "",
        channel: int = 1,
    ) -> dict:
        """Configure device as access point."""
        code = f"""
import network

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid={repr(ssid)}, password={repr(password)}, channel={channel})

config = ap.ifconfig()
print(repr({{
    'active': ap.active(),
    'ssid': {repr(ssid)},
    'ip': config[0],
    'netmask': config[1],
    'gateway': config[2],
}}))
"""
        result = await self.serial_manager.execute(port, code)

        try:
            for line in result.output.strip().split("\n"):
                if line.strip().startswith("{"):
                    return eval(line.strip())
        except Exception as e:
            logger.warning("Failed to parse AP config: %s", e)

        return {"active": False, "error": result.error or "Failed to configure AP"}

    async def save_config(
        self,
        port: str,
        ssid: str,
        password: str,
    ) -> bool:
        """Save WiFi configuration to boot.py for auto-connect."""
        boot_code = f'''
# WiFi auto-connect
import network
import time

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect({repr(ssid)}, {repr(password)})
        for _ in range(20):
            if wlan.isconnected():
                break
            time.sleep(0.5)
    return wlan.isconnected()

connect_wifi()
'''
        # Read existing boot.py
        try:
            content = await self.serial_manager.read_file(port, "/boot.py")
            existing = content.decode("utf-8", errors="replace")

            # Check if WiFi config already exists
            if "# WiFi auto-connect" in existing:
                # Replace existing config
                lines = existing.split("\n")
                new_lines = []
                skip_until_connect = False

                for line in lines:
                    if "# WiFi auto-connect" in line:
                        skip_until_connect = True
                        continue
                    if skip_until_connect:
                        if line.strip() == "connect_wifi()":
                            skip_until_connect = False
                        continue
                    new_lines.append(line)

                existing = "\n".join(new_lines).strip()

            # Append WiFi config
            new_content = existing + "\n\n" + boot_code

        except Exception:
            # No existing boot.py
            new_content = boot_code

        # Write updated boot.py
        return await self.serial_manager.write_file(
            port,
            "/boot.py",
            new_content.encode("utf-8"),
        )
