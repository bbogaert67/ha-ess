# Energy Flow Manager - UI Configuration Guide

This guide shows you how to configure the Energy Flow Manager integration through the Home Assistant user interface.

## Installation & Initial Setup

### Step 1: Add the Integration

1. Navigate to **Settings** → **Devices & Services**
2. Click the **+ ADD INTEGRATION** button (bottom right)
3. Search for "Energy Flow Manager"
4. Click on it to start the configuration wizard

![Add Integration](https://via.placeholder.com/800x400?text=Settings+%E2%86%92+Devices+%26+Services+%E2%86%92+Add+Integration)

---

## Configuration Wizard

The configuration wizard has 4 steps to make setup easy and organized:

### Step 1: Input Sensors Configuration

Configure the sensors that monitor your energy system.

**Screenshot: Input Sensors Step**
```
┌─────────────────────────────────────────────────────────┐
│  Energy Flow Manager - Input Sensors                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Configure the input sensors for monitoring energy      │
│  flows.                                                  │
│                                                          │
│  Solar Surplus Power Sensor (required) *                │
│  ┌────────────────────────────────────────────────┐    │
│  │ sensor.solar_surplus                      [▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Battery State of Charge Sensor (optional)              │
│  ┌────────────────────────────────────────────────┐    │
│  │ sensor.battery_soc                        [▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Battery Power Sensor (optional)                        │
│  ┌────────────────────────────────────────────────┐    │
│  │ sensor.battery_power                      [▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Water Temperature Sensor (optional)                    │
│  ┌────────────────────────────────────────────────┐    │
│  │ sensor.water_temperature                  [▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│                              [Cancel]  [Submit]         │
└─────────────────────────────────────────────────────────┘
```

**Fields:**
- **Solar Surplus Power Sensor** (required): Select the sensor that reports your solar surplus in Watts
  - Example: `sensor.solar_surplus`, `sensor.grid_power` (if negative = surplus)
  
- **Battery State of Charge Sensor** (optional): Select your battery SOC sensor (0-100%)
  - Example: `sensor.battery_soc`, `sensor.powerwall_charge`
  
- **Battery Power Sensor** (optional): Select your battery power flow sensor in Watts
  - Example: `sensor.battery_power` (positive = charging, negative = discharging)
  
- **Water Temperature Sensor** (optional): Select your water heater temperature sensor
  - Example: `sensor.water_heater_temperature`, `sensor.boiler_temp`

---

### Step 2: Water Heater Configuration

Configure how the water heater should be controlled.

**Screenshot: Water Heater Step**
```
┌─────────────────────────────────────────────────────────┐
│  Water Heater Configuration                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Configure water heater control settings.               │
│                                                          │
│  Water Heater Switch Entity (optional)                  │
│  ┌────────────────────────────────────────────────┐    │
│  │ switch.water_heater                       [▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Minimum Surplus to Start Heating (W)                   │
│  ┌────────────────────────────────────────────────┐    │
│  │ 2000                                      [▲▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Minimum Water Temperature (°C)                         │
│  ┌────────────────────────────────────────────────┐    │
│  │ 40                                        [▲▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Maximum Water Temperature (°C)                         │
│  ┌────────────────────────────────────────────────┐    │
│  │ 60                                        [▲▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Water Heater Power Consumption (W)                     │
│  ┌────────────────────────────────────────────────┐    │
│  │ 2000                                      [▲▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│                              [Cancel]  [Submit]         │
└─────────────────────────────────────────────────────────┘
```

**Fields:**
- **Water Heater Switch Entity**: Select the switch that controls your water heater
  - Example: `switch.water_heater`, `switch.boiler_relay`
  
- **Minimum Surplus to Start Heating**: Minimum solar surplus (in Watts) needed to turn on the heater
  - Default: 2000W
  - Range: 0-10000W
  
- **Minimum Water Temperature**: Temperature below which heating is allowed
  - Default: 40°C
  - Range: 0-100°C
  
- **Maximum Water Temperature**: Temperature at which heating stops
  - Default: 60°C
  - Range: 0-100°C
  
- **Water Heater Power Consumption**: How much power the heater uses (for surplus calculation)
  - Default: 2000W
  - Range: 0-10000W

---

### Step 3: Car Charger Configuration

Configure how the EV charger should be controlled.

**Screenshot: Car Charger Step**
```
┌─────────────────────────────────────────────────────────┐
│  Car Charger Configuration                              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Configure car charger control settings.                │
│                                                          │
│  Car Charger Switch Entity (optional)                   │
│  ┌────────────────────────────────────────────────┐    │
│  │ switch.car_charger                        [▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Car Charger Rate Control Entity (optional)             │
│  ┌────────────────────────────────────────────────┐    │
│  │ number.car_charger_max_current            [▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Minimum Surplus to Start Charging (W)                  │
│  ┌────────────────────────────────────────────────┐    │
│  │ 1400                                      [▲▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Minimum Charge Rate (A)                                │
│  ┌────────────────────────────────────────────────┐    │
│  │ 6                                         [▲▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Maximum Charge Rate (A)                                │
│  ┌────────────────────────────────────────────────┐    │
│  │ 16                                        [▲▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│                              [Cancel]  [Submit]         │
└─────────────────────────────────────────────────────────┘
```

**Fields:**
- **Car Charger Switch Entity**: Select the switch that controls your EV charger
  - Example: `switch.wallbox_charger`, `switch.easee_charger`
  
- **Car Charger Rate Control Entity**: Select the number entity that sets charge rate in Amperes
  - Example: `number.wallbox_max_current`, `number.easee_dynamic_current`
  
- **Minimum Surplus to Start Charging**: Minimum solar surplus needed to start charging
  - Default: 1400W (6A × 230V)
  - Range: 0-10000W
  
- **Minimum Charge Rate**: Minimum charging current in Amperes
  - Default: 6A (minimum for most chargers)
  - Range: 6-32A
  
- **Maximum Charge Rate**: Maximum charging current in Amperes
  - Default: 16A (standard household circuit)
  - Range: 6-32A

---

### Step 4: Battery & General Settings

Configure battery protection and update frequency.

**Screenshot: Battery & General Settings Step**
```
┌─────────────────────────────────────────────────────────┐
│  Battery & General Settings                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Configure battery protection and update settings.      │
│                                                          │
│  Minimum Battery SOC for Device Control (%)             │
│  ┌────────────────────────────────────────────────┐    │
│  │ 20                                        [▲▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Maximum Battery SOC (%)                                │
│  ┌────────────────────────────────────────────────┐    │
│  │ 90                                        [▲▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Update Interval (seconds)                              │
│  ┌────────────────────────────────────────────────┐    │
│  │ 30                                        [▲▼] │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│                              [Cancel]  [Submit]         │
└─────────────────────────────────────────────────────────┘
```

**Fields:**
- **Minimum Battery SOC for Device Control**: Devices won't turn on if battery is below this level
  - Default: 20%
  - Range: 0-100%
  - Purpose: Protects battery from excessive discharge
  
- **Maximum Battery SOC**: Reference value for battery management
  - Default: 90%
  - Range: 0-100%
  
- **Update Interval**: How often to check and update device states
  - Default: 30 seconds
  - Range: 10-300 seconds
  - Lower = more responsive, higher = less system load

---

## After Configuration

Once you complete all 4 steps, the integration will be added and you'll see:

1. **A new device** called "Energy Flow Manager" in your Devices & Services
2. **8 new sensors** for monitoring:
   - Solar Surplus
   - Battery SOC
   - Battery Power
   - Water Temperature
   - Available Surplus
   - Car Charger Rate
   - Water Heater Status
   - Car Charger Status

3. **A new service** `energy_flow_manager.force_update` for manual updates

---

## Reconfiguring the Integration

You can change settings at any time:

1. Go to **Settings** → **Devices & Services**
2. Find "Energy Flow Manager"
3. Click the **three dots** (⋮) menu
4. Select **Configure**
5. Update any settings you want to change
6. Click **Submit**

**Screenshot: Reconfigure Menu**
```
┌─────────────────────────────────────────────────────────┐
│  Energy Flow Manager                                    │
├─────────────────────────────────────────────────────────┤
│  ⋮  Options                                             │
│     ├─ Configure                                        │
│     ├─ Reload                                           │
│     ├─ System Options                                   │
│     └─ Delete                                           │
└─────────────────────────────────────────────────────────┘
```

---

## Options Configuration

The options menu allows you to update key parameters without re-entering all entity selections:

**Screenshot: Options Menu**
```
┌─────────────────────────────────────────────────────────┐
│  Energy Flow Manager Options                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Update configuration settings.                         │
│                                                          │
│  Minimum Surplus to Start Heating (W)                   │
│  │ 2000                                      [▲▼] │    │
│                                                          │
│  Minimum Water Temperature (°C)                         │
│  │ 40                                        [▲▼] │    │
│                                                          │
│  Maximum Water Temperature (°C)                         │
│  │ 60                                        [▲▼] │    │
│                                                          │
│  Minimum Surplus to Start Charging (W)                  │
│  │ 1400                                      [▲▼] │    │
│                                                          │
│  Minimum Charge Rate (A)                                │
│  │ 6                                         [▲▼] │    │
│                                                          │
│  Maximum Charge Rate (A)                                │
│  │ 16                                        [▲▼] │    │
│                                                          │
│  Minimum Battery SOC for Device Control (%)             │
│  │ 20                                        [▲▼] │    │
│                                                          │
│  Update Interval (seconds)                              │
│  │ 30                                        [▲▼] │    │
│                                                          │
│                              [Cancel]  [Submit]         │
└─────────────────────────────────────────────────────────┘
```

---

## Tips for Configuration

### Finding the Right Entities

**For Solar Surplus:**
- Look for sensors with "power", "grid", or "solar" in the name
- Should report in Watts (W)
- Positive values = surplus/export, Negative = import

**For Battery:**
- SOC sensors usually have "battery", "charge", or "soc" in the name
- Should report as percentage (0-100%)

**For Switches:**
- Look in the switch domain
- Common names: "water_heater", "boiler", "charger", "wallbox"

**For Number Entities (Charge Rate):**
- Look in the number domain
- Common names: "max_current", "charge_rate", "amperage"

### Recommended Settings

**Conservative (Battery Protection Priority):**
- Minimum Battery SOC: 30%
- Water Heater Min Surplus: 2500W
- Car Charger Min Surplus: 2000W

**Balanced (Default):**
- Minimum Battery SOC: 20%
- Water Heater Min Surplus: 2000W
- Car Charger Min Surplus: 1400W

**Aggressive (Maximum Solar Usage):**
- Minimum Battery SOC: 10%
- Water Heater Min Surplus: 1500W
- Car Charger Min Surplus: 1000W

---

## Troubleshooting Configuration

### "Entity not found" errors
- Make sure the entity exists in Home Assistant
- Check the entity ID is correct (Settings → Devices & Services → Entities)
- Restart Home Assistant if you just added new entities

### Devices not turning on
- Verify the minimum surplus threshold is not too high
- Check battery SOC is above minimum threshold
- Ensure the switch entities are working (test manually)

### Configuration not saving
- Check Home Assistant logs for errors
- Ensure you have write permissions to the config directory
- Try restarting Home Assistant

---

## Next Steps

After configuration:
1. Monitor the sensors to verify they're updating correctly
2. Create dashboard cards to visualize energy flows
3. Set up automations for notifications
4. Fine-tune thresholds based on your usage patterns

See the main README.md for dashboard examples and automation ideas!