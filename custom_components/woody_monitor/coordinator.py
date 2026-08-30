from __future__ import annotations

from datetime import timedelta
from typing import Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import WoodyMonitorApi, WoodyMonitorApiError
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL


class WoodyMonitorCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass, api: WoodyMonitorApi) -> None:
        super().__init__(
            hass,
            logger=__import__("logging").getLogger(__name__),
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            live = await self.api.get_live()
            # Settings are metadata + current editable values. If it fails,
            # live monitoring must still continue.
            try:
                settings = await self.api.get_controller_settings()
            except WoodyMonitorApiError:
                settings = {}
            return {"live": live, "settings": settings}
        except WoodyMonitorApiError as exc:
            raise UpdateFailed(str(exc)) from exc
