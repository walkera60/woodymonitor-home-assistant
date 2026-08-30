from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass

from .const import DOMAIN
from .entity import WoodyMonitorEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([WoodyMonitorConnection(coordinator, entry)])


class WoodyMonitorConnection(WoodyMonitorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry, "connection")
        self._attr_name = "Connection"

    @property
    def is_on(self):
        return bool(self.coordinator.data.get("live", {}).get("connected"))
