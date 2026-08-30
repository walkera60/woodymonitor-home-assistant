from __future__ import annotations

from homeassistant.components.button import ButtonEntity

from .const import DOMAIN
from .entity import WoodyMonitorEntity


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        WoodyMonitorCommandButton(data["coordinator"], entry, data["api"], "start", "Start burner"),
        WoodyMonitorCommandButton(data["coordinator"], entry, data["api"], "stop", "Stop burner"),
    ])


class WoodyMonitorCommandButton(WoodyMonitorEntity, ButtonEntity):
    def __init__(self, coordinator, entry, api, action, name):
        super().__init__(coordinator, entry, f"burner_{action}")
        self.api = api
        self.action = action
        self._attr_name = name

    async def async_press(self):
        await self.api.burner_command(self.action)
        await self.coordinator.async_request_refresh()
