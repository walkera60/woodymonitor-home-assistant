from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)

from .const import DOMAIN
from .entity import WoodyMonitorEntity


def _normal_alarm(value) -> bool:
    """Return True when the controller alarm represents a normal state."""
    if value is None:
        return True

    return str(value).strip().lower() in {
        "",
        "0",
        "ok",
        "none",
        "normal",
    }


def _burner_mode_is_fault(mode) -> bool:
    """Return True for controller modes that represent a burner fault."""
    if mode is None:
        return False

    mode = str(mode).strip()

    return (
        mode.startswith("Error -")
        or mode == "Burner connector plug removed"
    )


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async_add_entities(
        [
            WoodyMonitorConnection(coordinator, entry),
            WoodyMonitorBurnerFault(coordinator, entry),
            WoodyMonitorLowPellet(coordinator, entry),
        ]
    )


class WoodyMonitorConnection(WoodyMonitorEntity, BinarySensorEntity):
    """Woody Monitor API/controller connection."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry, "connection")
        self._attr_name = "Connection"

    @property
    def is_on(self):
        return bool(
            self.coordinator.data
            and self.coordinator.data.get("live", {}).get("connected")
        )


class WoodyMonitorBurnerFault(WoodyMonitorEntity, BinarySensorEntity):
    """Controller alarm or burner fault."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:fire-alert"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry, "burner_fault")
        self._attr_name = "Burner fault"

    @property
    def is_on(self):
        values = self.live_values

        alarm = values.get("alarm")
        mode = values.get("mode")

        return (
            not _normal_alarm(alarm)
            or _burner_mode_is_fault(mode)
        )

    @property
    def extra_state_attributes(self):
        values = self.live_values

        return {
            "alarm": values.get("alarm"),
            "mode": values.get("mode"),
            "power": values.get("power"),
            "power_kw": values.get("power_kW"),
            "boiler_temperature": values.get("boiler_temp"),
        }


class WoodyMonitorLowPellet(WoodyMonitorEntity, BinarySensorEntity):
    """Low pellet alarm reported by Woody Monitor."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:silo"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry, "low_pellet")
        self._attr_name = "Low pellet"

    @property
    def _alarm_data(self):
        if not self.coordinator.data:
            return {}

        return (
            self.coordinator.data
            .get("live", {})
            .get("low_pellet_alarm", {})
        )

    @property
    def is_on(self):
        return bool(self._alarm_data.get("active"))

    @property
    def extra_state_attributes(self):
        data = self._alarm_data

        return {
            "level_kg": data.get("level_kg"),
            "threshold_kg": data.get("threshold_kg"),
        }
