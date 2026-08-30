from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode

from .const import DOMAIN
from .entity import WoodyMonitorEntity
from .helpers import as_float, settings_map, unit


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    smap = settings_map(coordinator.data.get("settings", {}))

    entities = []
    for parameter, item in sorted(smap.items()):
        current = item.get("value", coordinator.data.get("live", {}).get("values", {}).get(parameter))
        minimum = item.get("min", item.get("minimum"))
        maximum = item.get("max", item.get("maximum"))
        decimals = item.get("decimals", 0)

        if as_float(current) is None:
            continue
        if as_float(minimum) is None or as_float(maximum) is None:
            continue
        if item.get("writable") is False:
            continue

        entities.append(
            WoodyMonitorNumber(
                coordinator, entry, data["api"], parameter, item
            )
        )

    async_add_entities(entities)


class WoodyMonitorNumber(WoodyMonitorEntity, NumberEntity):
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator, entry, api, parameter, metadata):
        super().__init__(coordinator, entry, parameter)
        self.api = api
        self.metadata = metadata
        self._attr_native_min_value = float(metadata.get("min", metadata.get("minimum")))
        self._attr_native_max_value = float(metadata.get("max", metadata.get("maximum")))
        decimals = int(metadata.get("decimals", 0) or 0)
        self._attr_native_step = 10 ** (-decimals) if decimals > 0 else 1
        self._attr_native_unit_of_measurement = unit(parameter)

    @property
    def native_value(self):
        item = settings_map(self.coordinator.data.get("settings", {})).get(self.parameter, {})
        value = item.get("value", self.live_values.get(self.parameter))
        return as_float(value)

    async def async_set_native_value(self, value: float):
        await self.api.set_controller_setting(self.parameter, value)
        await self.coordinator.async_request_refresh()
