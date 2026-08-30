from __future__ import annotations

from typing import Any


DISPLAY = {
    "boiler_temp": ("Boiler temperature", "°C"),
    "boiler_temp_set": ("Boiler temperature setpoint", "°C"),
    "boiler_temp_min": ("Minimum boiler temperature", "°C"),
    "boiler_temp_diff_down": ("Boiler temperature difference down", "°C"),
    "boiler_temp_diff_up": ("Boiler temperature difference up", "°C"),
    "boiler_return_temp": ("Boiler return temperature", "°C"),
    "hotwater_temp": ("Hot water temperature", "°C"),
    "hotwater_temp_set": ("Hot water temperature setpoint", "°C"),
    "hotwater_temp_diff": ("Hot water temperature difference", "°C"),
    "smoke_temp": ("Flue gas temperature", "°C"),
    "chute_temp": ("Chute temperature", "°C"),
    "chute_temp_max": ("Maximum chute temperature", "°C"),
    "outside_temp": ("Outdoor temperature", "°C"),
    "indoor_temp": ("Indoor temperature", "°C"),
    "oxygen": ("Oxygen", "%"),
    "power": ("Burner power", "%"),
    "power_kW": ("Burner power", "kW"),
    "flow": ("Flow", ""),
    "light": ("Light", ""),
    "feeder_time": ("Feeder runtime", "s"),
    "feeder_low": ("Feeder low", "%"),
    "feeder_high": ("Feeder high", "%"),
    "feed_per_minute": ("Feed per minute", "g/min"),
    "feeder_capacity": ("Feeder capacity", "g/6min"),
    "feeder_capacity_min": ("Minimum feeder capacity", "g/6min"),
    "feeder_capacity_max": ("Maximum feeder capacity", "g/6min"),
    "magazine_content": ("Magazine content", "kg"),
    "min_power": ("Minimum power", "%"),
    "max_power": ("Maximum power", "%"),
    "blower_low": ("Blower low", "%"),
    "blower_mid": ("Blower mid", "%"),
    "blower_high": ("Blower high", "%"),
    "blower_cleaning": ("Cleaning blower", "%"),
    "blower_off_time": ("Blower off time", "s"),
    "oxygen_low": ("Oxygen low", "%"),
    "oxygen_mid": ("Oxygen mid", "%"),
    "oxygen_high": ("Oxygen high", "%"),
    "mode": ("Burner mode", ""),
    "alarm": ("Alarm", ""),
    "version": ("Controller version", ""),
}


def friendly_name(parameter: str) -> str:
    if parameter in DISPLAY:
        return DISPLAY[parameter][0]
    return parameter.replace("_", " ").title()


def unit(parameter: str) -> str | None:
    value = DISPLAY.get(parameter, ("", ""))[1]
    return value or None


def as_float(value: Any) -> float | None:
    try:
        if value is None or isinstance(value, bool):
            return None
        return float(str(value).strip().replace(",", "."))
    except (TypeError, ValueError):
        return None


def iter_settings(payload: Any):
    """Flatten several possible Woody Monitor settings API shapes."""
    seen = set()

    def walk(obj: Any, key_hint: str | None = None):
        if isinstance(obj, dict):
            param = (
                obj.get("parameter")
                or obj.get("id")
                or obj.get("key")
                or obj.get("name") if any(k in obj for k in ("value", "min", "max", "minimum", "maximum", "decimals", "writable")) else None
            )
            if param and isinstance(param, str):
                item = dict(obj)
                item.setdefault("parameter", param)
                if param not in seen:
                    seen.add(param)
                    yield item
            for key, val in obj.items():
                if isinstance(val, dict):
                    if any(k in val for k in ("value", "min", "max", "minimum", "maximum", "decimals", "writable")):
                        item = dict(val)
                        item.setdefault("parameter", key)
                        if key not in seen:
                            seen.add(key)
                            yield item
                    else:
                        yield from walk(val, key)
                elif isinstance(val, list):
                    yield from walk(val, key)
        elif isinstance(obj, list):
            for val in obj:
                yield from walk(val, key_hint)

    yield from walk(payload)


def settings_map(payload: Any) -> dict[str, dict[str, Any]]:
    return {
        item["parameter"]: item
        for item in iter_settings(payload)
        if isinstance(item.get("parameter"), str)
    }
