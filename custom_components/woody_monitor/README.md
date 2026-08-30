# Woody Monitor Home Assistant integration

Local custom integration for Woody Monitor.

## Features

- Automatically creates sensors for every value returned by `/api/v1/live`.
- Connection binary sensor.
- Start/stop buttons.
- Burner switch.
- Dynamically creates editable Number entities from `/api/v1/controller/settings`.
- Dynamically creates Text entities for writable non-numeric settings such as timer values.
- Uses Woody Monitor's own validated controller API for writes. It does not access the serial port directly.
- Local polling every 5 seconds.

## Install

Copy:

`custom_components/woody_monitor`

to:

`/config/custom_components/woody_monitor`

on Home Assistant, then restart Home Assistant.

Go to:

Settings -> Devices & services -> Add integration -> Woody Monitor

Default URL:

`http://192.168.50.24:8080`

## Examples

After setup you should get entities such as:

- `sensor.woody_monitor_boiler_temperature`
- `sensor.woody_monitor_burner_power`
- `sensor.woody_monitor_outdoor_temperature`
- `sensor.woody_monitor_alarm`
- `number.woody_monitor_boiler_temperature_setpoint`
- `button.woody_monitor_start_burner`
- `button.woody_monitor_stop_burner`
- `switch.woody_monitor_burner`

Exact entity IDs are assigned by Home Assistant and may vary.

## Safety

Writes go through Woody Monitor's `/api/v1/controller/settings/<parameter>` endpoint,
so controller-side writable whitelist and min/max validation remain authoritative.
Start/stop uses `/api/v1/controller/burner/start|stop`.

The integration never communicates directly with the pellet controller serial port.
