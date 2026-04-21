# Energy Flow Manager for Home Assistant

A custom Home Assistant integration that intelligently manages energy flows by monitoring solar surplus power, battery state, and automatically controlling devices like water heaters and EV chargers to maximize self-consumption of solar energy.

## Features

- **Smart Energy Monitoring**: Tracks solar surplus, battery state of charge (SOC), battery power flow, and water temperature
- **Automated Water Heater Control**: Turns on water heater when surplus solar energy is available and water temperature is below target
- **Dynamic EV Charging**: Automatically starts/stops car charging and dynamically adjusts charge rate based on available surplus power
- **Battery Protection**: Configurable minimum battery SOC to prevent excessive battery discharge
- **Configurable Thresholds**: All parameters can be configured through the Home Assistant UI
- **Real-time Monitoring**: Provides sensors for all monitored values and device states
- **Priority Management**: Water heater has priority over car charging to ensure essential services

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/energy_flow_manager` directory to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration

### Initial Setup

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Energy Flow Manager"
4. Follow the configuration wizard:

#### Step 1: Input Sensors
- **Solar Surplus Power Sensor** (required): Entity that reports surplus solar power in Watts
- **Battery State of Charge Sensor** (optional): Entity that reports battery SOC in percentage
- **Battery Power Sensor** (optional): Entity that reports battery power flow in Watts
- **Water Temperature Sensor** (optional): Entity that reports water temperature in Celsius

#### Step 2: Water Heater Configuration
- **Water Heater Switch** (optional): Switch entity to control the water heater
- **Minimum Surplus to Start Heating**: Minimum solar surplus (W) required to turn on heater (default: 2000W)
- **Minimum Water Temperature**: Temperature below which heating is allowed (default: 40°C)
- **Maximum Water Temperature**: Temperature at which heating stops (default: 60°C)
- **Water Heater Power Consumption**: Power consumption of the heater (default: 2000W)

#### Step 3: Car Charger Configuration
- **Car Charger Switch** (optional): Switch entity to control the car charger
- **Car Charger Rate Control Entity** (optional): Number entity to set charge rate in Amperes
- **Minimum Surplus to Start Charging**: Minimum solar surplus (W) required to start charging (default: 1400W)
- **Minimum Charge Rate**: Minimum charge rate in Amperes (default: 6A)
- **Maximum Charge Rate**: Maximum charge rate in Amperes (default: 16A)

#### Step 4: Battery & General Settings
- **Minimum Battery SOC**: Minimum battery SOC (%) before devices are turned off (default: 20%)
- **Maximum Battery SOC**: Maximum battery SOC (%) (default: 90%)
- **Update Interval**: How often to update in seconds (default: 30s)

### Reconfiguration

You can modify settings at any time:
1. Go to **Settings** → **Devices & Services**
2. Find "Energy Flow Manager"
3. Click **Configure**

## Entities

The integration creates the following entities:

### Sensors

- `sensor.energy_flow_manager_solar_surplus`: Current solar surplus power (W)
- `sensor.energy_flow_manager_battery_soc`: Battery state of charge (%)
- `sensor.energy_flow_manager_battery_power`: Battery power flow (W)
- `sensor.energy_flow_manager_water_temperature`: Water temperature (°C)
- `sensor.energy_flow_manager_available_surplus`: Available surplus after device allocation (W)
- `sensor.energy_flow_manager_car_charger_rate`: Current car charging rate (A)
- `sensor.energy_flow_manager_water_heater_status`: Water heater status (Active/Inactive)
- `sensor.energy_flow_manager_car_charger_status`: Car charger status (Active/Inactive)

## Services

### `energy_flow_manager.force_update`

Forces an immediate update of energy flow calculations and device control.

**Example:**
```yaml
service: energy_flow_manager.force_update
```

## How It Works

### Priority System

1. **Water Heater** (Priority 1): Checked first. If conditions are met, it consumes its configured power from available surplus.
2. **Car Charger** (Priority 2): Uses remaining surplus after water heater allocation.

### Water Heater Logic

The water heater is turned ON when:
- Solar surplus ≥ configured minimum surplus
- Battery SOC ≥ configured minimum (if battery sensor configured)
- Water temperature < maximum temperature

The water heater is turned OFF when:
- Solar surplus < configured minimum surplus, OR
- Water temperature ≥ maximum temperature

### Car Charger Logic

The car charger is turned ON when:
- Available surplus (after water heater) ≥ configured minimum surplus
- Battery SOC ≥ configured minimum (if battery sensor configured)

**Dynamic Charge Rate Calculation:**
- Calculates optimal charge rate based on available surplus
- Formula: `Rate = min_rate + (available_surplus - min_power) / (max_power - min_power) * (max_rate - min_rate)`
- Assumes 230V single-phase: Power = Voltage × Current
- Rate is automatically adjusted between minimum and maximum configured values

The car charger is turned OFF when:
- Available surplus < configured minimum surplus

### Battery Protection

If a battery SOC sensor is configured:
- Devices will not turn on if battery SOC < configured minimum
- Prevents excessive battery discharge during low solar production

## Example Automations

### Notification When Water Heater Starts

```yaml
automation:
  - alias: "Notify Water Heater Started"
    trigger:
      - platform: state
        entity_id: sensor.energy_flow_manager_water_heater_status
        to: "Active"
    action:
      - service: notify.mobile_app
        data:
          message: "Water heater started using solar surplus"
```

### Dashboard Card Example

```yaml
type: entities
title: Energy Flow Manager
entities:
  - entity: sensor.energy_flow_manager_solar_surplus
  - entity: sensor.energy_flow_manager_battery_soc
  - entity: sensor.energy_flow_manager_available_surplus
  - entity: sensor.energy_flow_manager_water_heater_status
  - entity: sensor.energy_flow_manager_water_temperature
  - entity: sensor.energy_flow_manager_car_charger_status
  - entity: sensor.energy_flow_manager_car_charger_rate
```

## Troubleshooting

### Devices Not Turning On

1. Check that solar surplus sensor is reporting positive values
2. Verify battery SOC is above minimum threshold (if configured)
3. Check that device switch entities are correct and accessible
4. Review Home Assistant logs for error messages

### Charge Rate Not Changing

1. Verify the car charger rate entity is configured correctly
2. Check that the entity accepts number values in Amperes
3. Ensure your charger supports dynamic rate adjustment

### Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.energy_flow_manager: debug
```

## Requirements

- Home Assistant 2023.1 or newer
- Existing entities for:
  - Solar surplus power sensor
  - Device control switches (water heater, car charger)
  - Optional: Battery SOC sensor, water temperature sensor, car charger rate control

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check Home Assistant community forums

## License

This project is licensed under the MIT License.

## Credits

Developed for Home Assistant community to maximize solar self-consumption and reduce grid dependency.