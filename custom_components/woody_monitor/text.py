from __future__ import annotations

from homeassistant.components.text import TextEntity, TextMode

from .const import DOMAIN
from .entity import WoodyMonitorEntity
from .helpers import as_float, settings_map


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    smap = settings_map(coordinator.data.get("settings", {}))

    entities = []
    for parameter, item in sorted(smap.items()):
        current = item.get("value", coordinator.data.get("live", {}).get("values", {}).get(parameter))
        minimum = item.get("min", item.get("minimum"))
        maximum = item.get("max", item.get("maximum"))
        if item.get("writable") is False:
            continue

        # Non-numeric writable settings, e.g. HH:MM timer values.
        if as_float(current) is None and current is not None:
            entities.append(
                WoodyMonitorText(
                    coordinator, entry, data["api"], parameter
                )
            )

    async_add_entities(entities)


class WoodyMonitorText(WoodyMonitorEntity, TextEntity):
    _attr_mode = TextMode.TEXT
    _attr_native_min = 1
    _attr_native_max = 64

    def __init__(self, coordinator, entry, api, parameter):
        super().__init__(coordinator, entry, parameter)
        self.api = api

    @property
    def native_value(self):
        item = settings_map(self.coordinator.data.get("settings", {})).get(self.parameter, {})
        value = item.get("value", self.live_values.get(self.parameter))
        return None if value is None else str(value)

    async def async_set_value(self, value: str):
        await self.api.set_controller_setting(self.parameter, value)
        await self.coordinator.async_request_refresh()
