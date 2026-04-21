# Fixing Duplicate Energy Flow Manager Instances

## Problem
When adding the Energy Flow Manager integration, two instances were created instead of one.

## Root Cause
The config flow was missing single-instance enforcement. Version 1.0.5 fixes this issue.

## Solution - Update to v1.0.5

### Step 1: Remove All Existing Instances
1. Go to **Settings** → **Devices & Services**
2. Find all **Energy Flow Manager** entries
3. Click on each one and select **Delete**
4. Confirm deletion for all instances

### Step 2: Update the Integration via HACS
1. Go to **HACS** → **Integrations**
2. Find **Energy Flow Manager**
3. Click the **three dots menu** (⋮)
4. Select **Redownload** (this will get v1.0.5)
5. Wait for download to complete

### Step 3: Restart Home Assistant
1. Go to **Settings** → **System**
2. Click **Restart Home Assistant**
3. Wait for restart to complete

### Step 4: Add Integration (Only Once)
1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **Energy Flow Manager**
4. Click to add it
5. Configure all settings
6. Click **Submit**

### Step 5: Verify Single Instance
1. Go to **Settings** → **Devices & Services**
2. Verify only **ONE** Energy Flow Manager instance exists
3. Try to add it again - you should see an error message: "Already configured"

## What Changed in v1.0.5

The config flow now includes:
```python
# Check if already configured (single instance only)
await self.async_set_unique_id(DOMAIN)
self._abort_if_unique_id_configured()
```

This ensures:
- ✅ Only one instance can be created
- ✅ Attempting to add a second instance shows "Already configured" error
- ✅ No duplicate sensors or entities

## Alternative: Manual Installation Update

If you installed manually (not via HACS):

1. **Backup your configuration** (note down all entity selections and settings)
2. **Delete existing instances** from Settings → Devices & Services
3. **Update files**:
   ```bash
   cd /config/custom_components/energy_flow_manager
   git pull origin main
   ```
4. **Restart Home Assistant**
5. **Re-add the integration** with your saved configuration

## Verification

After updating, verify the fix worked:

1. **Check version**: HACS should show v1.0.5
2. **Single instance**: Only one Energy Flow Manager in Devices & Services
3. **Test duplicate prevention**: Try adding again - should fail with "Already configured"
4. **Sensors working**: All 8 sensors should be present and updating

## Expected Sensors (8 total)

After proper installation, you should see:
- `sensor.energy_flow_manager_solar_surplus`
- `sensor.energy_flow_manager_battery_soc`
- `sensor.energy_flow_manager_battery_power`
- `sensor.energy_flow_manager_water_temperature`
- `sensor.energy_flow_manager_available_surplus`
- `sensor.energy_flow_manager_car_charger_rate`
- `sensor.energy_flow_manager_water_heater_status`
- `sensor.energy_flow_manager_car_charger_status`

## Need Help?

If you still see duplicate instances after updating:
1. Remove ALL instances
2. Delete the integration folder: `/config/custom_components/energy_flow_manager`
3. Restart Home Assistant
4. Reinstall via HACS
5. Restart again
6. Add the integration

## Version History

- **v1.0.5**: Fixed duplicate instance creation (CRITICAL FIX)
- **v1.0.4**: Added enable/disable switches for devices
- **v1.0.3**: Removed switch platform
- **v1.0.2**: Added options flow for reconfiguration
- **v1.0.1**: Fixed invalid flow error
- **v1.0.0**: Initial release