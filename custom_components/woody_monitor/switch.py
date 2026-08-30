from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN
from .entity import WoodyMonitorEntity


STOPPED_MODES = {"stopped", "shut off", "summer stop", "off", "0"}


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        WoodyMonitorBurnerSwitch(data["coordinator"], entry, data["api"])
    ])


class WoodyMonitorBurnerSwitch(WoodyMonitorEntity, SwitchEntity):
    def __init__(self, coordinator, entry, api):
        super().__init__(coordinator, entry, "burner")
        self.api = api
        self._attr_name = "Burner"

    @property
    def is_on(self):
        mode = self.live_values.get("mode")
        if mode is None:
            return None
        return str(mode).strip().lower() not in STOPPED_MODES

    async def async_turn_on(self, **kwargs):
        await self.api.burner_command("start")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.api.burner_command("stop")
        await self.coordinator.async_request_refresh()
