"""Type stubs for ntptime module (NTP time synchronization)."""

# NTP server (can be changed)
host: str

def settime() -> None:
    """Synchronize system time with NTP server.

    Connects to NTP server and sets the RTC to UTC time.

    Example:
        import ntptime
        import network

        # Connect to WiFi first
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect('ssid', 'password')

        # Sync time
        ntptime.settime()

    Raises:
        OSError: If network connection fails
    """
    ...


def time() -> int:
    """Get current NTP time without setting RTC.

    Returns:
        Unix timestamp (seconds since 1970-01-01)
    """
    ...
