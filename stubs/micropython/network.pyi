"""Type stubs for MicroPython network module."""

from typing import Any, Optional, Tuple, Union, overload

# Interface constants
STA_IF: int
AP_IF: int

# Auth modes
AUTH_OPEN: int
AUTH_WEP: int
AUTH_WPA_PSK: int
AUTH_WPA2_PSK: int
AUTH_WPA_WPA2_PSK: int
AUTH_WPA2_ENTERPRISE: int
AUTH_WPA3_PSK: int
AUTH_WPA2_WPA3_PSK: int

# Status codes
STAT_IDLE: int
STAT_CONNECTING: int
STAT_WRONG_PASSWORD: int
STAT_NO_AP_FOUND: int
STAT_CONNECT_FAIL: int
STAT_GOT_IP: int

# PHY modes
MODE_11B: int
MODE_11G: int
MODE_11N: int
MODE_LR: int

def hostname(name: Optional[str] = None) -> str:
    """Get or set the network hostname."""
    ...

def country(code: Optional[str] = None) -> str:
    """Get or set the WiFi country code."""
    ...

def phy_mode(mode: Optional[int] = None) -> int:
    """Get or set the PHY mode."""
    ...


class WLAN:
    """WiFi interface class."""

    # For backward compatibility
    PM_NONE: int
    PM_PERFORMANCE: int
    PM_POWERSAVE: int

    def __init__(self, interface_id: int) -> None:
        """Create WLAN interface.

        Args:
            interface_id: STA_IF for station or AP_IF for access point
        """
        ...

    def active(self, is_active: Optional[bool] = None) -> bool:
        """Activate or deactivate the interface.

        Args:
            is_active: True to activate, False to deactivate, None to query

        Returns:
            Current active state
        """
        ...

    def connect(
        self,
        ssid: Optional[str] = None,
        key: Optional[str] = None,
        *,
        bssid: Optional[bytes] = None,
        timeout: Optional[int] = None
    ) -> None:
        """Connect to a WiFi network.

        Args:
            ssid: Network name
            key: Password (or None for open networks)
            bssid: MAC address of access point
            timeout: Connection timeout in milliseconds
        """
        ...

    def disconnect(self) -> None:
        """Disconnect from the current network."""
        ...

    def isconnected(self) -> bool:
        """Check if connected to a network.

        Returns:
            True if connected and has IP address
        """
        ...

    def status(self, param: Optional[str] = None) -> Union[int, str]:
        """Get connection status.

        Args:
            param: Optional parameter name ('rssi', 'stations', etc.)

        Returns:
            Status code or parameter value
        """
        ...

    def scan(self) -> list[Tuple[bytes, bytes, int, int, int, bool]]:
        """Scan for available networks.

        Returns:
            List of tuples: (ssid, bssid, channel, RSSI, authmode, hidden)
        """
        ...

    @overload
    def ifconfig(self) -> Tuple[str, str, str, str]:
        """Get network configuration.

        Returns:
            Tuple of (ip, subnet, gateway, dns)
        """
        ...

    @overload
    def ifconfig(
        self,
        config: Union[str, Tuple[str, str, str, str]]
    ) -> None:
        """Set network configuration.

        Args:
            config: 'dhcp' for DHCP, or tuple of (ip, subnet, gateway, dns)
        """
        ...

    def config(self, param: str) -> Any:
        """Get configuration parameter.

        Args:
            param: Parameter name ('mac', 'essid', 'channel', etc.)
        """
        ...

    @overload
    def config(self, **kwargs: Any) -> None:
        """Set configuration parameters.

        Supported kwargs:
            essid: Network name (AP mode)
            channel: WiFi channel
            hidden: Hide SSID (AP mode)
            password: Network password (AP mode)
            authmode: Authentication mode
            protocol: PHY protocol
            pm: Power management mode
            txpower: Transmit power
            mac: MAC address
        """
        ...


class LAN:
    """Ethernet LAN interface."""

    PHY_LAN8720: int
    PHY_IP101: int
    PHY_RTL8201: int
    PHY_DP83848: int
    PHY_KSZ8041: int
    PHY_KSZ8081: int

    ETH_INITIALIZED: int
    ETH_STARTED: int
    ETH_STOPPED: int
    ETH_CONNECTED: int
    ETH_DISCONNECTED: int
    ETH_GOT_IP: int

    def __init__(
        self,
        *,
        id: int = 0,
        mdc: int = ...,
        mdio: int = ...,
        power: Optional[int] = None,
        phy_type: int = PHY_LAN8720,
        phy_addr: int = 0,
        ref_clk: Optional[int] = None,
        ref_clk_mode: Optional[int] = None
    ) -> None:
        """Create LAN interface.

        Args:
            id: Interface ID
            mdc: MDC pin
            mdio: MDIO pin
            power: Power control pin
            phy_type: PHY chip type
            phy_addr: PHY address
            ref_clk: Reference clock pin
            ref_clk_mode: Reference clock mode
        """
        ...

    def active(self, is_active: Optional[bool] = None) -> bool:
        """Activate or deactivate the interface."""
        ...

    def isconnected(self) -> bool:
        """Check if connected."""
        ...

    def status(self) -> int:
        """Get connection status."""
        ...

    def ifconfig(
        self,
        config: Optional[Union[str, Tuple[str, str, str, str]]] = None
    ) -> Optional[Tuple[str, str, str, str]]:
        """Get or set network configuration."""
        ...

    def config(self, param: Optional[str] = None, **kwargs: Any) -> Any:
        """Get or set configuration parameters."""
        ...


class PPP:
    """Point-to-Point Protocol interface."""

    def __init__(self, stream: Any) -> None:
        """Create PPP interface from a stream."""
        ...

    def active(self, is_active: Optional[bool] = None) -> bool:
        """Activate or deactivate the interface."""
        ...

    def isconnected(self) -> bool:
        """Check if connected."""
        ...

    def status(self) -> int:
        """Get connection status."""
        ...

    def ifconfig(
        self,
        config: Optional[Tuple[str, str, str, str]] = None
    ) -> Optional[Tuple[str, str, str, str]]:
        """Get or set network configuration."""
        ...

    def connect(
        self,
        authmode: int = ...,
        username: str = ...,
        password: str = ...
    ) -> None:
        """Connect using PPP."""
        ...

    def disconnect(self) -> None:
        """Disconnect PPP."""
        ...
