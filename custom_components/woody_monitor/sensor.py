from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfPower,
    PERCENTAGE,
    UnitOfTime,
    UnitOfMass,
)
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN
from .entity import WoodyMonitorEntity
from .helpers import as_float, unit


def _native_unit(parameter: str):
    u = unit(parameter)
    if u == "°C":
        return UnitOfTemperature.CELSIUS
    if u == "kW":
        return UnitOfPower.KILO_WATT
    if u == "%":
        return PERCENTAGE
    if u == "s":
        return UnitOfTime.SECONDS
    if u == "kg":
        return UnitOfMass.KILOGRAMS
    return u


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    values = coordinator.data.get("live", {}).get("values", {})
    async_add_entities(
        WoodyMonitorSensor(coordinator, entry, parameter)
        for parameter in sorted(values)
    )


class WoodyMonitorSensor(WoodyMonitorEntity, SensorEntity):
    def __init__(self, coordinator, entry, parameter):
        super().__init__(coordinator, entry, parameter)
        self._attr_native_unit_of_measurement = _native_unit(parameter)

    @property
    def native_value(self):
        value = self.live_values.get(self.parameter)
        numeric = as_float(value)
        return numeric if numeric is not None else value

    @property
    def extra_state_attributes(self):
        return {"parameter": self.parameter}
