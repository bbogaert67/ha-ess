# Troubleshooting: Sensors Showing No Data

## Problem
After installing Energy Flow Manager, the sensors pane shows no data or sensors appear as "unavailable" or "unknown".

## Common Causes and Solutions

### 1. Entity IDs Not Configured
**Symptom**: All sensors show "unavailable" or "unknown"

**Solution**:
1. Go to **Settings** → **Devices & Services**
2. Find **Energy Flow Manager**
3. Click **Configure** (gear icon)
4. Verify all required entity IDs are selected:
   - **Solar Surplus Sensor** (required)
   - Battery SOC Sensor (optional)
   - Battery Power Sensor (optional)
   - Water Temperature Sensor (optional)
   - Water Heater Switch (optional)
   - Car Charger Switch (optional)
   - Car Charger Rate Entity (optional)

### 2. Selected Entities Don't Exist
**Symptom**: Some sensors show data, others don't

**Check**:
1. Go to **Developer Tools** → **States**
2. Search for the entity IDs you configured
3. Verify they exist and have valid states

**Solution**:
- If entities don't exist, reconfigure with correct entity IDs
- Make sure entity IDs are spelled correctly (case-sensitive)

### 3. Selected Entities Have Invalid States
**Symptom**: Sensors exist but show "unavailable"

**Check Entity States**:
```
Developer Tools → States
Look for your configured entities:
- State should be a number (not "unavailable" or "unknown")
- Example: "2500" for solar surplus in watts
```

**Solution**:
- Fix the source entities first
- Once source entities have valid data, Energy Flow Manager will update

### 4. Update Interval Too Long
**Symptom**: Sensors eventually show data but take a long time

**Solution**:
1. Go to **Settings** → **Devices & Services**
2. Find **Energy Flow Manager** → **Configure**
3. Set **Update Interval** to a lower value (e.g., 30 seconds)
4. Click **Submit**

### 5. Integration Not Reloaded After Configuration Change
**Symptom**: Changed configuration but sensors still show old/no data

**Solution** (v1.0.6+):
- Configuration changes now automatically reload the integration
- If using older version, manually restart Home Assistant

**Manual Reload**:
1. Go to **Developer Tools** → **Services**
2. Call service: `homeassistant.reload_config_entry`
3. Service data:
   ```yaml
   entry_id: [your_energy_flow_manager_entry_id]
   ```

### 6. Check Home Assistant Logs
**View Logs**:
1. Go to **Settings** → **System** → **Logs**
2. Search for "energy_flow_manager"
3. Look for errors or warnings

**Common Log Messages**:
```
WARNING: Could not convert state of sensor.xxx to float: unavailable
→ The source sensor is unavailable

ERROR: Entity sensor.xxx not found
→ Wrong entity ID configured

INFO: Force update triggered
→ Manual update successful
```

## Diagnostic Steps

### Step 1: Verify Integration is Loaded
```
Settings → Devices & Services → Energy Flow Manager
Should show: "1 device, 8 entities"
```

### Step 2: Check Sensor Entities
Go to **Developer Tools** → **States** and search for:
- `sensor.energy_flow_manager_solar_surplus`
- `sensor.energy_flow_manager_battery_soc`
- `sensor.energy_flow_manager_battery_power`
- `sensor.energy_flow_manager_water_temperature`
- `sensor.energy_flow_manager_available_surplus`
- `sensor.energy_flow_manager_car_charger_rate`
- `sensor.energy_flow_manager_water_heater_status`
- `sensor.energy_flow_manager_car_charger_status`

### Step 3: Force Update
1. Go to **Developer Tools** → **Services**
2. Call service: `energy_flow_manager.force_update`
3. Check if sensors update

### Step 4: Check Source Entities
For each configured entity, verify in **Developer Tools** → **States**:
- Entity exists
- State is a valid number (not "unavailable", "unknown", or text)
- State updates regularly

## Example Valid Configuration

```yaml
Solar Surplus Sensor: sensor.solar_power_surplus
Battery SOC Sensor: sensor.battery_state_of_charge
Battery Power Sensor: sensor.battery_power
Water Temperature Sensor: sensor.water_heater_temperature
Water Heater Switch: switch.water_heater
Car Charger Switch: switch.car_charger
Car Charger Rate Entity: number.car_charger_current
```

**Expected States**:
- `sensor.solar_power_surplus`: "2500" (watts)
- `sensor.battery_state_of_charge`: "85" (percent)
- `sensor.battery_power`: "-1200" (watts, negative = charging)
- `sensor.water_heater_temperature`: "45" (°C)
- `switch.water_heater`: "on" or "off"
- `switch.car_charger`: "on" or "off"
- `number.car_charger_current`: "16" (amps)

## Still Not Working?

### Complete Reset
1. **Remove Integration**:
   - Settings → Devices & Services → Energy Flow Manager → Delete
2. **Restart Home Assistant**
3. **Verify Source Entities**:
   - Developer Tools → States
   - Confirm all entities you plan to use exist and have valid data
4. **Reinstall Integration**:
   - Settings → Devices & Services → Add Integration
   - Search "Energy Flow Manager"
   - Configure with verified entity IDs
5. **Check Sensors**:
   - Wait 30 seconds (default update interval)
   - Developer Tools → States
   - Search "energy_flow_manager"

### Enable Debug Logging
Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.energy_flow_manager: debug
```

Restart Home Assistant and check logs for detailed information.

## Configuration Changes Not Applied?

**Issue**: Changed configuration but nothing happens

**Solution** (v1.0.6+):
- Configuration changes now trigger automatic reload
- No manual restart needed

**For older versions**:
1. After changing configuration, restart Home Assistant
2. Or use Developer Tools → Services → `homeassistant.reload_config_entry`

## Need More Help?

1. **Check GitHub Issues**: https://github.com/bbogaert67/ha-ess/issues
2. **Create New Issue** with:
   - Home Assistant version
   - Energy Flow Manager version
   - Configuration (entity IDs)
   - Relevant log entries
   - Screenshots of sensor states