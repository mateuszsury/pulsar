"""MicroPython library manager - search, download, and install packages.

Supports multiple package sources:
- Built-in quick packages (verified MicroPython libraries)
- micropython-lib official repository
- PyPI micropython-* packages
- Custom GitHub repositories
"""

import asyncio
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import quote, urljoin

if TYPE_CHECKING:
    from serial_comm.manager import SerialManager

logger = logging.getLogger(__name__)

# MicroPython package sources
MICROPYTHON_LIB_INDEX = "https://micropython.org/pi/v2/index.json"
MICROPYTHON_LIB_RAW = "https://raw.githubusercontent.com/micropython/micropython-lib/master"
PYPI_SEARCH_API = "https://pypi.org/pypi/{package}/json"
PYPI_SIMPLE_INDEX = "https://pypi.org/simple/"


@dataclass
class PackageInfo:
    """Package information."""

    name: str = ""
    version: str = ""
    description: str = ""
    author: str = ""
    license: str = ""
    url: str = ""
    source: str = ""  # 'quick', 'micropython-lib', 'pypi', 'github'
    dependencies: list[str] = field(default_factory=list)
    installed: bool = False
    available_versions: list[str] = field(default_factory=list)
    files: list[tuple[str, str]] = field(default_factory=list)
    note: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "license": self.license,
            "url": self.url,
            "source": self.source,
            "dependencies": self.dependencies,
            "installed": self.installed,
            "available_versions": self.available_versions,
            "note": self.note,
        }


@dataclass
class InstallProgress:
    """Package installation progress."""

    status: str = "idle"
    package: str = ""
    progress: float = 0.0
    message: str = ""
    error: str = ""

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "package": self.package,
            "progress": self.progress,
            "message": self.message,
            "error": self.error,
        }


class LibraryManager:
    """MicroPython library manager with multi-source support."""

    # ==========================================================================
    # QUICK PACKAGES - Verified MicroPython libraries with direct download URLs
    # ==========================================================================
    QUICK_PACKAGES: dict[str, dict[str, Any]] = {
        # MQTT
        "umqtt.simple": {
            "description": "Simple MQTT client for MicroPython",
            "category": "networking",
            "files": [
                ("lib/umqtt/simple.py", f"{MICROPYTHON_LIB_RAW}/micropython/umqtt.simple/umqtt/simple.py"),
                ("lib/umqtt/__init__.py", ""),
            ],
        },
        "umqtt.robust": {
            "description": "Robust MQTT client with auto-reconnect",
            "category": "networking",
            "files": [
                ("lib/umqtt/robust.py", f"{MICROPYTHON_LIB_RAW}/micropython/umqtt.robust/umqtt/robust.py"),
                ("lib/umqtt/__init__.py", ""),
            ],
            "dependencies": ["umqtt.simple"],
        },

        # HTTP
        "urequests": {
            "description": "HTTP requests library (sync)",
            "category": "networking",
            "files": [
                ("lib/urequests.py", f"{MICROPYTHON_LIB_RAW}/micropython/urequests/urequests.py"),
            ],
        },
        "aiohttp": {
            "description": "Async HTTP client library",
            "category": "networking",
            "files": [
                ("lib/aiohttp/__init__.py", f"{MICROPYTHON_LIB_RAW}/python-ecosys/aiohttp/aiohttp/__init__.py"),
            ],
        },

        # Time & Scheduling
        "ntptime": {
            "description": "NTP time synchronization",
            "category": "time",
            "files": [
                ("lib/ntptime.py", f"{MICROPYTHON_LIB_RAW}/micropython/ntptime/ntptime.py"),
            ],
        },

        # Displays
        "ssd1306": {
            "description": "SSD1306 OLED display driver (I2C/SPI)",
            "category": "display",
            "files": [
                ("lib/ssd1306.py", f"{MICROPYTHON_LIB_RAW}/micropython/ssd1306/ssd1306.py"),
            ],
        },
        "ssd1309": {
            "description": "SSD1309 OLED display driver",
            "category": "display",
            "files": [
                ("lib/ssd1309.py", "https://raw.githubusercontent.com/rdagger/micropython-ssd1309/master/ssd1309.py"),
            ],
        },
        "sh1106": {
            "description": "SH1106 OLED display driver",
            "category": "display",
            "files": [
                ("lib/sh1106.py", "https://raw.githubusercontent.com/robert-hh/SH1106/master/sh1106.py"),
            ],
        },
        "st7789": {
            "description": "ST7789 TFT display driver",
            "category": "display",
            "files": [
                ("lib/st7789.py", "https://raw.githubusercontent.com/russhughes/st7789_mpy/master/st7789.py"),
            ],
        },
        "ili9341": {
            "description": "ILI9341 TFT display driver",
            "category": "display",
            "files": [
                ("lib/ili9341.py", "https://raw.githubusercontent.com/rdagger/micropython-ili9341/master/ili9341.py"),
            ],
        },
        "max7219": {
            "description": "MAX7219 LED matrix/7-segment driver",
            "category": "display",
            "files": [
                ("lib/max7219.py", "https://raw.githubusercontent.com/mcauser/micropython-max7219/master/max7219.py"),
            ],
        },
        "tm1637": {
            "description": "TM1637 7-segment LED display driver",
            "category": "display",
            "files": [
                ("lib/tm1637.py", "https://raw.githubusercontent.com/mcauser/micropython-tm1637/master/tm1637.py"),
            ],
        },

        # Sensors - Temperature/Humidity
        "bme280": {
            "description": "BME280 temperature/humidity/pressure sensor",
            "category": "sensor",
            "files": [
                ("lib/bme280.py", "https://raw.githubusercontent.com/robert-hh/BME280/master/bme280_int.py"),
            ],
        },
        "bme680": {
            "description": "BME680 environmental sensor",
            "category": "sensor",
            "files": [
                ("lib/bme680.py", "https://raw.githubusercontent.com/robert-hh/BME680-Micropython/master/bme680.py"),
            ],
        },
        "bmp280": {
            "description": "BMP280 barometric pressure sensor",
            "category": "sensor",
            "files": [
                ("lib/bmp280.py", "https://raw.githubusercontent.com/dafvid/micropython-bmp280/master/bmp280.py"),
            ],
        },
        "ahtx0": {
            "description": "AHT10/AHT20 temperature/humidity sensor",
            "category": "sensor",
            "files": [
                ("lib/ahtx0.py", "https://raw.githubusercontent.com/targetblank/micropython_ahtx0/master/ahtx0.py"),
            ],
        },
        "sht30": {
            "description": "SHT30 temperature/humidity sensor",
            "category": "sensor",
            "files": [
                ("lib/sht30.py", "https://raw.githubusercontent.com/rsc1975/micropython-sht30/master/sht30.py"),
            ],
        },
        "htu21d": {
            "description": "HTU21D temperature/humidity sensor",
            "category": "sensor",
            "files": [
                ("lib/htu21d.py", "https://raw.githubusercontent.com/randymxj/Adafruit-HTU21D-MicroPython/master/htu21d.py"),
            ],
        },

        # Sensors - Motion/Position
        "mpu6050": {
            "description": "MPU6050 accelerometer/gyroscope",
            "category": "sensor",
            "files": [
                ("lib/mpu6050.py", "https://raw.githubusercontent.com/adamjezek98/MPU6050-ESP8266-MicroPython/master/mpu6050.py"),
            ],
        },
        "mpu9250": {
            "description": "MPU9250 9-axis motion sensor",
            "category": "sensor",
            "files": [
                ("lib/mpu9250.py", "https://raw.githubusercontent.com/tuupola/micropython-mpu9250/master/mpu9250.py"),
            ],
        },
        "hmc5883l": {
            "description": "HMC5883L magnetometer/compass",
            "category": "sensor",
            "files": [
                ("lib/hmc5883l.py", "https://raw.githubusercontent.com/gvalkov/micropython-esp8266-hmc5883l/master/hmc5883l.py"),
            ],
        },

        # Sensors - Light/Color
        "bh1750": {
            "description": "BH1750 ambient light sensor",
            "category": "sensor",
            "files": [
                ("lib/bh1750.py", "https://raw.githubusercontent.com/PinkInk/upylib/master/bh1750/bh1750.py"),
            ],
        },
        "tcs34725": {
            "description": "TCS34725 RGB color sensor",
            "category": "sensor",
            "files": [
                ("lib/tcs34725.py", "https://raw.githubusercontent.com/adafruit/micropython-adafruit-tcs34725/master/tcs34725.py"),
            ],
        },

        # Sensors - Distance
        "hcsr04": {
            "description": "HC-SR04 ultrasonic distance sensor",
            "category": "sensor",
            "files": [
                ("lib/hcsr04.py", "https://raw.githubusercontent.com/rsc1975/micropython-hcsr04/master/hcsr04.py"),
            ],
        },
        "vl53l0x": {
            "description": "VL53L0X laser distance sensor",
            "category": "sensor",
            "files": [
                ("lib/vl53l0x.py", "https://raw.githubusercontent.com/uceeatz/VL53L0X/main/vl53l0x.py"),
            ],
        },

        # Motor/Servo Control
        "pca9685": {
            "description": "PCA9685 16-channel PWM/servo driver",
            "category": "motor",
            "files": [
                ("lib/pca9685.py", "https://raw.githubusercontent.com/adafruit/micropython-adafruit-pca9685/master/pca9685.py"),
            ],
        },
        "servo": {
            "description": "Simple servo motor control",
            "category": "motor",
            "files": [
                ("lib/servo.py", f"{MICROPYTHON_LIB_RAW}/micropython/servo/servo.py"),
            ],
        },
        "l298n": {
            "description": "L298N motor driver",
            "category": "motor",
            "files": [
                ("lib/l298n.py", "https://raw.githubusercontent.com/kevinmcaleer/micropython_motor_library/main/motor.py"),
            ],
        },
        "stepper": {
            "description": "Stepper motor control (ULN2003, A4988)",
            "category": "motor",
            "files": [
                ("lib/stepper.py", "https://raw.githubusercontent.com/redoxcode/micropython-stepper/main/stepper.py"),
            ],
        },

        # Communication/Protocols
        "micropython-ld2410": {
            "description": "LD2410 radar sensor driver",
            "category": "sensor",
            "files": [
                ("lib/ld2410.py", "https://raw.githubusercontent.com/DigiDuncan/micropython-ld2410/main/ld2410.py"),
            ],
        },
        "micropython-modbus": {
            "description": "Modbus RTU/TCP client",
            "category": "communication",
            "files": [
                ("lib/umodbus/__init__.py", "https://raw.githubusercontent.com/brainelectronics/micropython-modbus/main/umodbus/__init__.py"),
                ("lib/umodbus/common.py", "https://raw.githubusercontent.com/brainelectronics/micropython-modbus/main/umodbus/common.py"),
                ("lib/umodbus/modbus.py", "https://raw.githubusercontent.com/brainelectronics/micropython-modbus/main/umodbus/modbus.py"),
                ("lib/umodbus/serial.py", "https://raw.githubusercontent.com/brainelectronics/micropython-modbus/main/umodbus/serial.py"),
            ],
        },

        # Storage
        "sdcard": {
            "description": "SD card driver (SPI)",
            "category": "storage",
            "files": [
                ("lib/sdcard.py", f"{MICROPYTHON_LIB_RAW}/micropython/drivers/sdcard/sdcard.py"),
            ],
        },

        # Encoders/Input
        "rotary": {
            "description": "Rotary encoder driver",
            "category": "input",
            "files": [
                ("lib/rotary.py", "https://raw.githubusercontent.com/miketeachman/micropython-rotary/master/rotary.py"),
                ("lib/rotary_irq_esp.py", "https://raw.githubusercontent.com/miketeachman/micropython-rotary/master/rotary_irq_esp.py"),
            ],
        },
        "keypad": {
            "description": "Matrix keypad driver",
            "category": "input",
            "files": [
                ("lib/keypad.py", "https://raw.githubusercontent.com/mcauser/micropython-tm1638/master/keypad.py"),
            ],
        },

        # RTC
        "ds1307": {
            "description": "DS1307 RTC module",
            "category": "time",
            "files": [
                ("lib/ds1307.py", "https://raw.githubusercontent.com/mcauser/micropython-ds1307/master/ds1307.py"),
            ],
        },
        "ds3231": {
            "description": "DS3231 high-precision RTC module",
            "category": "time",
            "files": [
                ("lib/ds3231.py", "https://raw.githubusercontent.com/mcauser/micropython-ds3231/master/ds3231.py"),
            ],
        },
        "pcf8563": {
            "description": "PCF8563 RTC module",
            "category": "time",
            "files": [
                ("lib/pcf8563.py", "https://raw.githubusercontent.com/lewisxhe/PCF8563_PythonLibrary/master/pcf8563.py"),
            ],
        },

        # Audio
        "dfplayer": {
            "description": "DFPlayer Mini MP3 player",
            "category": "audio",
            "files": [
                ("lib/dfplayer.py", "https://raw.githubusercontent.com/ShrimpingIt/micropython-dfplayer/master/dfplayer.py"),
            ],
        },

        # Power/ADC
        "ina219": {
            "description": "INA219 current/voltage sensor",
            "category": "power",
            "files": [
                ("lib/ina219.py", "https://raw.githubusercontent.com/chrisb2/pyb_ina219/master/ina219.py"),
            ],
        },
        "ads1x15": {
            "description": "ADS1115/ADS1015 ADC",
            "category": "adc",
            "files": [
                ("lib/ads1x15.py", "https://raw.githubusercontent.com/robert-hh/ads1x15/master/ads1x15.py"),
            ],
        },

        # RFID
        "mfrc522": {
            "description": "MFRC522 RFID reader",
            "category": "rfid",
            "files": [
                ("lib/mfrc522.py", "https://raw.githubusercontent.com/wendlers/micropython-mfrc522/master/mfrc522.py"),
            ],
        },

        # I/O Expanders
        "pcf8574": {
            "description": "PCF8574 I2C GPIO expander",
            "category": "io",
            "files": [
                ("lib/pcf8574.py", "https://raw.githubusercontent.com/mcauser/micropython-pcf8574/master/pcf8574.py"),
            ],
        },
        "mcp23017": {
            "description": "MCP23017 I2C GPIO expander",
            "category": "io",
            "files": [
                ("lib/mcp23017.py", "https://raw.githubusercontent.com/mcauser/micropython-mcp23017/master/mcp23017.py"),
            ],
        },

        # Web/API
        "microdot": {
            "description": "Minimalist web framework",
            "category": "web",
            "files": [
                ("lib/microdot.py", "https://raw.githubusercontent.com/miguelgrinberg/microdot/main/src/microdot/microdot.py"),
            ],
        },
        "picoweb": {
            "description": "Pico web framework (async)",
            "category": "web",
            "files": [
                ("lib/picoweb/__init__.py", f"{MICROPYTHON_LIB_RAW}/python-ecosys/picoweb/picoweb/__init__.py"),
            ],
        },

        # Built-in (no installation needed)
        "uasyncio": {
            "description": "Async I/O library (built-in on MicroPython 1.13+)",
            "category": "core",
            "files": [],
            "note": "Built-in module, no installation needed",
        },
        "dht": {
            "description": "DHT11/DHT22 temperature/humidity sensor (built-in)",
            "category": "sensor",
            "files": [],
            "note": "Built-in module on ESP32/ESP8266",
        },
        "neopixel": {
            "description": "NeoPixel/WS2812 LED driver (built-in)",
            "category": "led",
            "files": [],
            "note": "Built-in module on ESP32/ESP8266",
        },
        "onewire": {
            "description": "OneWire protocol driver (built-in)",
            "category": "protocol",
            "files": [],
            "note": "Built-in module on ESP32/ESP8266",
        },
        "ds18x20": {
            "description": "DS18x20 temperature sensor driver (built-in)",
            "category": "sensor",
            "files": [],
            "note": "Built-in module on ESP32/ESP8266",
        },
        "framebuf": {
            "description": "Frame buffer manipulation (built-in)",
            "category": "display",
            "files": [],
            "note": "Built-in module",
        },
        "bluetooth": {
            "description": "Bluetooth/BLE (built-in)",
            "category": "wireless",
            "files": [],
            "note": "Built-in module on ESP32",
        },
        "espnow": {
            "description": "ESP-NOW protocol (built-in)",
            "category": "wireless",
            "files": [],
            "note": "Built-in module on ESP32/ESP8266",
        },
    }

    # Package categories for UI organization
    CATEGORIES = {
        "networking": "Networking & Communication",
        "display": "Displays & LEDs",
        "sensor": "Sensors",
        "motor": "Motors & Servos",
        "time": "Time & RTC",
        "storage": "Storage",
        "input": "Input Devices",
        "audio": "Audio",
        "power": "Power Management",
        "adc": "ADC/DAC",
        "rfid": "RFID & NFC",
        "io": "I/O Expanders",
        "web": "Web & API",
        "communication": "Communication Protocols",
        "core": "Core/Built-in",
        "wireless": "Wireless",
        "led": "LEDs",
        "protocol": "Protocols",
    }

    def __init__(self, serial_manager: "SerialManager") -> None:
        self.serial_manager = serial_manager
        self._progress = InstallProgress()
        self._index_cache: dict[str, Any] = {}
        self._pypi_cache: dict[str, PackageInfo] = {}
        self._micropython_lib_cache: list[PackageInfo] = []
        self._cache_dir = Path.home() / ".pulsar" / "package_cache"
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._index_loaded = False

    def get_progress(self) -> dict:
        """Get current installation progress."""
        return self._progress.to_dict()

    # ==========================================================================
    # SEARCH & LISTING
    # ==========================================================================

    async def search_packages(
        self,
        query: str,
        include_pypi: bool = True,
        include_micropython_lib: bool = True,
    ) -> list[PackageInfo]:
        """Search for packages across all sources."""
        packages: list[PackageInfo] = []
        query_lower = query.lower()

        # 1. Search quick packages
        for name, info in self.QUICK_PACKAGES.items():
            if (query_lower in name.lower() or
                query_lower in info.get("description", "").lower() or
                query_lower in info.get("category", "").lower()):
                pkg = PackageInfo(
                    name=name,
                    description=info.get("description", ""),
                    source="quick",
                    note=info.get("note", ""),
                    dependencies=info.get("dependencies", []),
                )
                packages.append(pkg)

        # 2. Search micropython-lib index
        if include_micropython_lib:
            mplib_results = await self._search_micropython_lib(query)
            packages.extend(mplib_results)

        # 3. Search PyPI for micropython packages
        if include_pypi:
            pypi_results = await self._search_pypi(query)
            packages.extend(pypi_results)

        # Remove duplicates (prefer quick packages)
        seen = set()
        unique_packages = []
        for pkg in packages:
            key = pkg.name.lower().replace("-", "_").replace("micropython_", "").replace("micropython-", "")
            if key not in seen:
                seen.add(key)
                unique_packages.append(pkg)

        return unique_packages

    async def list_available(self, category: str | None = None) -> list[PackageInfo]:
        """List all available packages, optionally filtered by category."""
        packages = []

        for name, info in self.QUICK_PACKAGES.items():
            if category and info.get("category") != category:
                continue

            pkg = PackageInfo(
                name=name,
                description=info.get("description", ""),
                source="quick",
                note=info.get("note", ""),
                dependencies=info.get("dependencies", []),
            )
            packages.append(pkg)

        return sorted(packages, key=lambda p: p.name)

    def list_categories(self) -> dict[str, str]:
        """List all package categories."""
        return self.CATEGORIES.copy()

    async def list_installed(self, port: str) -> list[PackageInfo]:
        """List installed packages on device."""
        packages = []

        try:
            # List files in /lib directory
            files = await self.serial_manager.list_files(port, "/lib")

            for file in files:
                name = file.get("name", "")
                if name.endswith(".py") or file.get("is_dir", False):
                    pkg_name = name.rstrip(".py")
                    pkg = PackageInfo(
                        name=pkg_name,
                        installed=True,
                    )
                    # Try to get info from quick packages
                    if pkg_name in self.QUICK_PACKAGES:
                        info = self.QUICK_PACKAGES[pkg_name]
                        pkg.description = info.get("description", "")
                        pkg.source = "quick"
                    packages.append(pkg)
        except Exception as e:
            logger.warning("Could not list installed packages: %s", e)

        return packages

    # ==========================================================================
    # MICROPYTHON-LIB SEARCH
    # ==========================================================================

    async def _load_micropython_lib_index(self) -> None:
        """Load the micropython-lib package index."""
        if self._micropython_lib_cache:
            return

        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    MICROPYTHON_LIB_INDEX,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self._parse_micropython_lib_index(data)
        except Exception as e:
            logger.warning("Could not load micropython-lib index: %s", e)

    def _parse_micropython_lib_index(self, data: dict) -> None:
        """Parse micropython-lib index into PackageInfo list."""
        packages = data.get("packages", [])
        for pkg_data in packages:
            name = pkg_data.get("name", "")
            if name and name not in self.QUICK_PACKAGES:
                pkg = PackageInfo(
                    name=name,
                    version=pkg_data.get("version", ""),
                    description=pkg_data.get("description", ""),
                    source="micropython-lib",
                    url=pkg_data.get("url", ""),
                )
                self._micropython_lib_cache.append(pkg)

    async def _search_micropython_lib(self, query: str) -> list[PackageInfo]:
        """Search micropython-lib index."""
        await self._load_micropython_lib_index()

        results = []
        query_lower = query.lower()

        for pkg in self._micropython_lib_cache:
            if (query_lower in pkg.name.lower() or
                query_lower in pkg.description.lower()):
                results.append(pkg)

        return results[:20]  # Limit results

    # ==========================================================================
    # PYPI SEARCH
    # ==========================================================================

    async def _search_pypi(self, query: str) -> list[PackageInfo]:
        """Search PyPI for micropython-related packages."""
        import aiohttp

        results = []

        # Search for common micropython package prefixes
        search_terms = [
            f"micropython-{query}",
            f"micropython_{query}",
        ]

        try:
            async with aiohttp.ClientSession() as session:
                for term in search_terms:
                    try:
                        url = PYPI_SEARCH_API.format(package=quote(term))
                        async with session.get(
                            url,
                            timeout=aiohttp.ClientTimeout(total=10)
                        ) as response:
                            if response.status == 200:
                                data = await response.json()
                                pkg = self._parse_pypi_package(data)
                                if pkg:
                                    results.append(pkg)
                    except Exception:
                        continue
        except Exception as e:
            logger.warning("PyPI search error: %s", e)

        return results

    def _parse_pypi_package(self, data: dict) -> PackageInfo | None:
        """Parse PyPI package JSON into PackageInfo."""
        info = data.get("info", {})
        name = info.get("name", "")

        if not name:
            return None

        # Only include packages that are likely MicroPython compatible
        summary = info.get("summary", "").lower()
        keywords = info.get("keywords", "").lower() if info.get("keywords") else ""

        if not any(kw in summary + keywords for kw in ["micropython", "esp32", "esp8266", "pico"]):
            return None

        return PackageInfo(
            name=name,
            version=info.get("version", ""),
            description=info.get("summary", ""),
            author=info.get("author", ""),
            license=info.get("license", ""),
            url=info.get("home_page", "") or info.get("project_url", ""),
            source="pypi",
        )

    # ==========================================================================
    # INSTALLATION
    # ==========================================================================

    async def install_package(
        self,
        port: str,
        package_name: str,
        force: bool = False,
        version: str | None = None,
    ) -> bool:
        """Install a package on the device."""
        self._progress = InstallProgress(
            status="starting",
            package=package_name,
            message=f"Installing {package_name}...",
        )

        try:
            # 1. Check if it's a quick package
            if package_name in self.QUICK_PACKAGES:
                return await self._install_quick_package(port, package_name, force)

            # 2. Try using mip on the device (micropython-lib)
            success = await self._install_with_mip(port, package_name)
            if success:
                return True

            # 3. Try upip as fallback
            return await self._install_with_upip(port, package_name)

        except Exception as e:
            logger.exception("Package installation error: %s", e)
            self._progress = InstallProgress(
                status="error",
                package=package_name,
                error=str(e),
            )
            return False

    async def _install_quick_package(
        self,
        port: str,
        package_name: str,
        force: bool = False,
    ) -> bool:
        """Install a quick package (verified MicroPython library)."""
        pkg_info = self.QUICK_PACKAGES[package_name]

        # Check if it's a built-in module
        if not pkg_info.get("files"):
            self._progress = InstallProgress(
                status="complete",
                package=package_name,
                progress=1.0,
                message=pkg_info.get("note", "Built-in module, no installation needed"),
            )
            return True

        # Install dependencies first
        for dep in pkg_info.get("dependencies", []):
            self._progress.message = f"Installing dependency: {dep}"
            await self.install_package(port, dep, force)

        # Create /lib directory if needed
        await self._ensure_lib_dir(port)

        # Download and install files
        files = pkg_info["files"]
        total_files = len(files)

        for i, (remote_path, url) in enumerate(files):
            self._progress.progress = (i + 1) / (total_files + 1)
            self._progress.message = f"Installing {remote_path}..."

            # Ensure directory exists
            dir_path = "/".join(remote_path.split("/")[:-1])
            if dir_path:
                await self._ensure_dir(port, "/" + dir_path)

            if url:
                # Download file
                content = await self._download_file(url)
                if content is None:
                    raise RuntimeError(f"Failed to download {url}")

                # Upload to device
                success = await self.serial_manager.write_file(
                    port, "/" + remote_path, content
                )
                if not success:
                    raise RuntimeError(f"Failed to write {remote_path}")
            else:
                # Create empty init file
                await self.serial_manager.write_file(
                    port, "/" + remote_path, b""
                )

        self._progress = InstallProgress(
            status="complete",
            package=package_name,
            progress=1.0,
            message=f"Successfully installed {package_name}",
        )
        return True

    async def _install_with_mip(self, port: str, package_name: str) -> bool:
        """Try to install package using mip on the device."""
        self._progress.message = f"Installing {package_name} via mip..."

        code = f"""
import mip
try:
    mip.install('{package_name}')
    print('SUCCESS')
except Exception as e:
    print('ERROR:', e)
"""
        result = await self.serial_manager.execute(port, code, timeout=120)

        if "SUCCESS" in result.output:
            self._progress = InstallProgress(
                status="complete",
                package=package_name,
                progress=1.0,
                message=f"Successfully installed {package_name}",
            )
            return True
        return False

    async def _install_with_upip(self, port: str, package_name: str) -> bool:
        """Try to install package using upip on the device."""
        self._progress.message = f"Installing {package_name} via upip..."

        code = f"""
import upip
try:
    upip.install('{package_name}')
    print('SUCCESS')
except Exception as e:
    print('ERROR:', e)
"""
        result = await self.serial_manager.execute(port, code, timeout=120)

        if "SUCCESS" in result.output:
            self._progress = InstallProgress(
                status="complete",
                package=package_name,
                progress=1.0,
                message=f"Successfully installed {package_name}",
            )
            return True
        else:
            self._progress = InstallProgress(
                status="error",
                package=package_name,
                error=f"Package not found: {package_name}",
            )
            return False

    async def install_from_github(
        self,
        port: str,
        repo_url: str,
        path: str = "",
    ) -> bool:
        """Install a package from GitHub repository."""
        self._progress = InstallProgress(
            status="starting",
            package=repo_url,
            message=f"Installing from GitHub...",
        )

        try:
            # Parse GitHub URL
            match = re.match(
                r"https?://github\.com/([^/]+)/([^/]+)(?:/tree/([^/]+))?(/.*)?",
                repo_url
            )
            if not match:
                raise ValueError("Invalid GitHub URL")

            owner, repo, branch, subpath = match.groups()
            branch = branch or "main"
            subpath = subpath or ""

            # Use mip to install from GitHub
            mip_url = f"github:{owner}/{repo}"
            if subpath:
                mip_url += subpath

            return await self._install_with_mip(port, mip_url)

        except Exception as e:
            self._progress = InstallProgress(
                status="error",
                package=repo_url,
                error=str(e),
            )
            return False

    # ==========================================================================
    # UNINSTALLATION
    # ==========================================================================

    async def uninstall_package(self, port: str, package_name: str) -> bool:
        """Uninstall a package from the device."""
        self._progress = InstallProgress(
            status="uninstalling",
            package=package_name,
            message=f"Uninstalling {package_name}...",
        )

        try:
            # Try to delete the package file or directory
            paths_to_try = [
                f"/lib/{package_name}.py",
                f"/lib/{package_name}",
                f"/{package_name}.py",
            ]

            for path in paths_to_try:
                try:
                    await self.serial_manager.delete_file(port, path)
                    self._progress = InstallProgress(
                        status="complete",
                        package=package_name,
                        progress=1.0,
                        message=f"Uninstalled {package_name}",
                    )
                    return True
                except Exception:
                    continue

            self._progress = InstallProgress(
                status="error",
                package=package_name,
                error=f"Package {package_name} not found",
            )
            return False

        except Exception as e:
            self._progress = InstallProgress(
                status="error",
                package=package_name,
                error=str(e),
            )
            return False

    # ==========================================================================
    # UTILITIES
    # ==========================================================================

    async def _ensure_lib_dir(self, port: str) -> None:
        """Ensure /lib directory exists."""
        await self._ensure_dir(port, "/lib")

    async def _ensure_dir(self, port: str, path: str) -> None:
        """Ensure a directory exists on the device."""
        try:
            await self.serial_manager.mkdir(port, path)
        except Exception:
            pass  # Directory may already exist

    async def _download_file(self, url: str) -> bytes | None:
        """Download a file from URL."""
        import aiohttp

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        return await response.read()
                    logger.error("Download failed: %s (status %d)", url, response.status)
                    return None
        except Exception as e:
            logger.exception("Download error: %s", e)
            return None

    def get_package_info(self, package_name: str) -> PackageInfo | None:
        """Get information about a package."""
        if package_name in self.QUICK_PACKAGES:
            info = self.QUICK_PACKAGES[package_name]
            return PackageInfo(
                name=package_name,
                description=info.get("description", ""),
                source="quick",
                dependencies=info.get("dependencies", []),
                note=info.get("note", ""),
            )
        return None
