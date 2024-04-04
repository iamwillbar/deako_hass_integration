"""Constants for Deako."""
# Base component constants
NAME = "Deako Smart Lighting"
DOMAIN = "deako"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.2"
ATTRIBUTION = ""
ISSUE_URL = "https://github.com/sebirdman/deako_hass_integration/issues"

# Icons
ICON = "mdi:format-quote-close"

# Platforms
LIGHT = "light"
PLATFORMS = [LIGHT]

# Configuration and options
CONF_ENABLED = "enabled"
CONF_IP = "ip"

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration for Deako!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
