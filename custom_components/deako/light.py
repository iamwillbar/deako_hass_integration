"""Light platform for deako."""
from .const import (
    DOMAIN,
    NAME,
)

import logging

from homeassistant.components.light import (
    ATTR_BRIGHTNESS, LightEntity, ColorMode)
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.util.color import value_to_brightness
from homeassistant.util.percentage import percentage_to_ranged_value


BRIGHTNESS_SCALE = (0, 255)
_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Configure the platform."""
    client = hass.data[DOMAIN][entry.entry_id]

    devices = client.get_devices()
    for uuid in devices:
        async_add_devices([DeakoLightSwitch(client, uuid)])


class DeakoLightSwitch(LightEntity):
    """Deako LightEntity class."""

    def __init__(self, connection, uuid):
        self.connection = connection
        self.uuid = uuid
        self.connection.set_state_callback(self.uuid, self.on_update)

    def on_update(self):
        self.schedule_update_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, self.unique_id)
            },
            name=self.name,
            manufacturer=NAME,
        )

    @property
    def unique_id(self):
        """Return the ID of this Deako light."""
        return self.uuid

    @property
    def name(self):
        """Return the name of the Deako light."""
        return self.connection.get_name_for_device(self.uuid)

    @property
    def is_on(self):
        """Return true if the lihgt is on."""
        state = self.connection.get_state_for_device(self.uuid)
        return state["power"]

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        state = self.connection.get_state_for_device(self.uuid)
        if state["dim"] is None:
            return None
        return value_to_brightness(BRIGHTNESS_SCALE, state["dim"])

    @property
    def supported_color_modes(self):
        """Return the color modes supported by this light."""
        state = self.connection.get_state_for_device(self.uuid)
        if state["dim"] is None:
            return [ColorMode.ONOFF]
        return [ColorMode.BRIGHTNESS]

    @property
    def color_mode(self):
        """Return the color mode of this light."""
        state = self.connection.get_state_for_device(self.uuid)
        if state["dim"] is None:
            return ColorMode.ONOFF
        return ColorMode.BRIGHTNESS

    async def async_turn_on(self, **kwargs):
        state = self.connection.get_state_for_device(self.uuid)
        dim = 100
        if state["dim"] is not None:
            dim = state["dim"]
        if ATTR_BRIGHTNESS in kwargs:
            dim = percentage_to_ranged_value(BRIGHTNESS_SCALE, kwargs[ATTR_BRIGHTNESS])
        await self.connection.send_device_control(self.uuid, True, round(dim, 0))

    async def async_turn_off(self, **kwargs):
        state = self.connection.get_state_for_device(self.uuid)
        dim = 100
        if state["dim"] is not None:
            dim = state["dim"]
        if ATTR_BRIGHTNESS in kwargs:
            dim = percentage_to_ranged_value(BRIGHTNESS_SCALE, kwargs[ATTR_BRIGHTNESS])
        await self.connection.send_device_control(self.uuid, False, round(dim, 0))
