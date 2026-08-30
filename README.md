# Woody Monitor for Home Assistant

Home Assistant integration for Woody Monitor pellet burner systems.

## Features

- Local connection to Woody Monitor
- Automatic discovery of live burner parameters
- Temperature sensors
- Burner power and operating data
- Controller connection status
- Controller settings exposed to Home Assistant
- Burner start and stop controls
- Local polling without cloud services

## Installation with HACS

1. Open HACS in Home Assistant.
2. Add this repository as a custom repository.
3. Select category `Integration`.
4. Install `Woody Monitor`.
5. Restart Home Assistant.
6. Go to Settings → Devices & services.
7. Select Add integration.
8. Search for `Woody Monitor`.
9. Enter the Woody Monitor URL.

Example:

http://192.168.50.24:8080

## Requirements

A running Woody Monitor installation reachable from Home Assistant.

## Safety

Controller changes and burner commands are sent through the Woody Monitor API.
The integration does not communicate directly with the pellet burner serial interface.
