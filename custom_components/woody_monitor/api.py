from __future__ import annotations

from typing import Any
from urllib.parse import quote

from aiohttp import ClientSession, ClientResponseError


class WoodyMonitorApiError(Exception):
    """Woody Monitor API error."""


class WoodyMonitorApi:
    def __init__(self, session: ClientSession, base_url: str) -> None:
        self._session = session
        self.base_url = base_url.rstrip("/")

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        try:
            async with self._session.request(
                method,
                url,
                params=params,
                json=json_data,
                timeout=10,
            ) as response:
                response.raise_for_status()
                if response.content_type == "application/json":
                    return await response.json()
                text = await response.text()
                return {"result": text}
        except Exception as exc:
            raise WoodyMonitorApiError(str(exc)) from exc

    async def get_status(self) -> dict[str, Any]:
        return await self._request("GET", "/api/v1/status")

    async def get_live(self) -> dict[str, Any]:
        return await self._request("GET", "/api/v1/live")

    async def get_controller_settings(self) -> Any:
        return await self._request("GET", "/api/v1/controller/settings")

    async def set_controller_setting(self, parameter: str, value: Any) -> Any:
        # Woody Monitor's existing controller settings API accepts value as query data.
        return await self._request(
            "POST",
            f"/api/v1/controller/settings/{quote(parameter, safe='')}",
            params={"value": str(value)},
        )

    async def burner_command(self, action: str) -> Any:
        if action not in {"start", "stop"}:
            raise WoodyMonitorApiError(f"Unsupported burner action: {action}")
        return await self._request(
            "POST",
            f"/api/v1/controller/burner/{action}",
        )
