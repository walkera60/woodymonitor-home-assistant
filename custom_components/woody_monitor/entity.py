from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .helpers import friendly_name


class WoodyMonitorEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, parameter: str) -> None:
        super().__init__(coordinator)
        self.entry = entry
        self.parameter = parameter
        self._attr_unique_id = f"{entry.entry_id}_{parameter}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": "Woody Monitor",
            "manufacturer": "Woody / NBE",
            "model": "Pellet burner controller",
            "configuration_url": self.entry.data["url"],
        }

    @property
    def name(self):
        return friendly_name(self.parameter)

    @property
    def live_values(self):
        return (
            self.coordinator.data.get("live", {}).get("values", {})
            if self.coordinator.data
            else {}
        )
