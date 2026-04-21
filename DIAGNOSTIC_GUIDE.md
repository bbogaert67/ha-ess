# Energy Flow Manager - Diagnostic Guide

## Current Issues and Solutions

### Issue 1: Two Water Temperature Sensors

**Problem**: Two water temperature sensors appear in the system.

**Cause**: Old sensor from previous installation wasn't removed.

**Solution**:
1. Go to **Settings** → **Devices & Services**
2. Find **Energy Flow Manager**
3. Click on it to see all entities
4. Look for duplicate water temperature sensors
5. Delete the old one (usually has a different entity ID)
6. Or: Delete the entire integration and reinstall fresh

### Issue 2: Car Charger Rate Shows 6 Instead of 0

**Problem**: Car Charger Rate sensor shows 6A even when charger is inactive.

**Cause**: Rate was being calculated but not reset to 0 when charger turns off.

**Fixed in v1.0.10**: Rate now correctly shows 0 when charger is inactive.

### Issue 3: Status Sensors Show "Inactive"

**Problem**: Water Heater Status and Car Charger Status both show "Inactive" when they should be active.

**Possible Causes**:

#### A. Solar Surplus Too Low
Check your solar surplus value:
1. Go to **Developer Tools** → **States**
2. Find your configured solar surplus sensor
3. Check its current value

**Requirements**:
- Water Heater: Needs ≥ 2000W by default (configurable)
- Car Charger: Needs ≥ 1400W by default (configurable)

**Solution**: If surplus is too low, either:
- Wait for more solar production
- Lower the minimum surplus thresholds in configuration

#### B. Water Temperature Issues
For water heater to activate:
- Water temp must be < max temp (default 60°C)
- Water temp sensor must have valid data

Check:
1. **Developer Tools** → **States**
2. Find your water temperature sensor
3. Verify it shows a number (not "unavailable" or "unknown")
4. Check if temp is below your configured max (default 60°C)

#### C. Battery SOC Too Low
If you configured a battery SOC sensor:
- Battery must be ≥ minimum SOC (default 20%)

Check:
1. **Developer Tools** → **States**
2. Find your battery SOC sensor
3. Verify it's above minimum threshold

**Solution**: If battery is too low:
- Wait for battery to charge
- Lower the minimum battery SOC in configuration
- Or don't configure a battery SOC sensor (makes it optional)

#### D. Entities Not Configured
Check your configuration:
1. **Settings** → **Devices & Services** → **Energy Flow Manager** → **Configure**
2. Verify all required entities are selected:
   - Solar Surplus Sensor (REQUIRED)
   - Water Heater Switch (if you want water heater control)
   - Car Charger Switch (if you want car charger control)
3. Optional entities:
   - Battery SOC Sensor
   - Battery Power Sensor
   - Water Temperature Sensor
   - Car Charger Rate Entity

#### E. Enable/Disable Switches
Check if devices are enabled:
1. **Settings** → **Devices & Services** → **Energy Flow Manager** → **Configure**
2. Look for:
   - "Enable Water Heater Control" - must be ON
   - "Enable Car Charger Control" - must be ON

### Issue 4: Understanding Status Values

**Status Sensors Show**:
- "Active" = Device should be ON (logic says turn on)
- "Inactive" = Device should be OFF (logic says turn off)

**This is DIFFERENT from the actual switch state**:
- Status sensor = What the integration WANTS to do
- Switch entity = What the device IS actually doing

**Example**:
- Status: "Active" + Switch: "off" = Integration wants to turn it on but hasn't yet (or switch failed)
- Status: "Inactive" + Switch: "on" = Integration wants to turn it off but hasn't yet

## Diagnostic Steps

### Step 1: Check All Source Entities

Go to **Developer Tools** → **States** and verify:

```
sensor.your_solar_surplus → Should show a number (e.g., "2500")
sensor.your_battery_soc → Should show a number (e.g., "85")
sensor.your_water_temp → Should show a number (e.g., "45")
switch.your_water_heater → Should show "on" or "off"
switch.your_car_charger → Should show "on" or "off"
```

### Step 2: Check Energy Flow Manager Sensors

```
sensor.energy_flow_manager_solar_surplus → Should match your source
sensor.energy_flow_manager_battery_soc → Should match your source
sensor.energy_flow_manager_water_temperature → Should match your source
sensor.energy_flow_manager_available_surplus → Calculated value
sensor.energy_flow_manager_car_charger_rate → 0-32A
sensor.energy_flow_manager_water_heater_status → Active/Inactive
sensor.energy_flow_manager_car_charger_status → Active/Inactive
```

### Step 3: Check Configuration Values

Go to **Settings** → **Devices & Services** → **Energy Flow Manager** → **Configure**

**Water Heater Settings**:
- Minimum Surplus: Default 2000W
- Minimum Temperature: Default 40°C
- Maximum Temperature: Default 60°C
- Heater Power: Default 2000W

**Car Charger Settings**:
- Minimum Surplus: Default 1400W
- Minimum Rate: Default 6A
- Maximum Rate: Default 16A

**Battery Settings**:
- Minimum SOC: Default 20%
- Maximum SOC: Default 90%

### Step 4: Check Logs

1. Go to **Settings** → **System** → **Logs**
2. Search for "energy_flow_manager"
3. Look for messages like:
   - "Turned on water heater (surplus: X W, temp: Y°C)"
   - "Turned off water heater (surplus: X W, temp: Y°C)"
   - "Turned on car charger (surplus: X W, rate: Y A)"
   - "Turned off car charger (surplus: X W)"

### Step 5: Force Update

Try forcing an update:
1. **Developer Tools** → **Services**
2. Call service: `energy_flow_manager.force_update`
3. Check if sensors update

### Step 6: Enable Debug Logging

Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.energy_flow_manager: debug
```

Restart Home Assistant and check logs for detailed information.

## Common Scenarios

### Scenario 1: Everything Shows "Inactive"

**Check**:
1. Solar surplus value - is it high enough?
2. All source entities - do they have valid data?
3. Enable switches - are both devices enabled?

**Most Common Cause**: Solar surplus is below minimum thresholds.

**Solution**: Lower the minimum surplus values in configuration or wait for more solar production.

### Scenario 2: Water Heater Active, Car Charger Inactive

**This is NORMAL** if:
- Water heater is using most of the surplus
- Not enough surplus left for car charger
- Water heater has priority over car charger

**Example**:
- Solar surplus: 2500W
- Water heater needs: 2000W
- Available for car: 500W
- Car charger needs minimum: 1400W
- Result: Water heater ON, car charger OFF

### Scenario 3: Both Inactive Despite Good Surplus

**Check**:
1. Battery SOC - is it above minimum?
2. Water temperature - is it below maximum?
3. Entity IDs - are they correct in configuration?

### Scenario 4: Status Says "Active" But Switch is "Off"

**Possible Causes**:
1. Switch entity doesn't exist or is unavailable
2. Switch is controlled by another automation
3. Physical device is offline
4. Permissions issue (Home Assistant can't control the switch)

**Check**:
1. Manually toggle the switch in Home Assistant
2. Check if switch responds
3. Check switch entity state in Developer Tools

## Need More Help?

If issues persist after following this guide:

1. **Gather Information**:
   - Current solar surplus value
   - Current battery SOC (if configured)
   - Current water temperature (if configured)
   - All configuration values (thresholds)
   - Screenshots of sensor states
   - Relevant log entries

2. **Create GitHub Issue**: https://github.com/bbogaert67/ha-ess/issues

3. **Include**:
   - Home Assistant version
   - Energy Flow Manager version
   - Diagnostic information from above
   - What you expect vs what you see