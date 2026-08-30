from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import WoodyMonitorApi, WoodyMonitorApiError
from .const import CONF_URL, DEFAULT_URL, DOMAIN


class WoodyMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            url = user_input[CONF_URL].strip().rstrip("/")
            try:
                api = WoodyMonitorApi(async_get_clientsession(self.hass), url)
                status = await api.get_status()
                if status.get("application") != "Woody Monitor":
                    errors["base"] = "not_woody_monitor"
                else:
                    await self.async_set_unique_id(url)
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(
                        title="Woody Monitor",
                        data={CONF_URL: url},
                    )
            except WoodyMonitorApiError:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_URL, default=DEFAULT_URL): str}
            ),
            errors=errors,
        )
