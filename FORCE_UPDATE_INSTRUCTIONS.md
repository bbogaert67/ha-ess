# Force Update to v1.0.7 - Critical Fix Required

## Current Situation
You're still running an old version with the AttributeError bug, even though v1.0.7 is available on GitHub.

## Why HACS Shows Commit Hash
**This is normal**: HACS displays the git commit hash (e.g., `cc7013e`) for tracking purposes. The actual version (1.0.7) is in the manifest.json file. Both are correct - the commit hash is just how HACS identifies the exact code version.

## Force Update Steps

### Method 1: Complete Reinstall (Recommended)

1. **Delete Integration Instance**
   - Settings → Devices & Services
   - Find "Energy Flow Manager"
   - Click on it → Delete
   - Confirm deletion

2. **Remove from HACS**
   - HACS → Integrations
   - Find "Energy Flow Manager"
   - Three dots menu (⋮) → Remove
   - Confirm removal

3. **Clear Browser Cache**
   - Press Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
   - Or clear browser cache completely

4. **Restart Home Assistant**
   - Settings → System → Restart

5. **Reinstall via HACS**
   - HACS → Integrations
   - Click "+ Explore & Download Repositories"
   - Search "Energy Flow Manager"
   - Click Download
   - Select latest version
   - Click Download again

6. **Restart Home Assistant Again**
   - Settings → System → Restart

7. **Add Integration**
   - Settings → Devices & Services
   - Click "+ Add Integration"
   - Search "Energy Flow Manager"
   - Configure with your entities
   - Click Submit

### Method 2: Manual File Update

1. **SSH into Home Assistant** or use File Editor add-on

2. **Navigate to custom components**
   ```bash
   cd /config/custom_components/energy_flow_manager
   ```

3. **Backup current files**
   ```bash
   cp sensor.py sensor.py.backup
   ```

4. **Download latest sensor.py**
   ```bash
   wget https://raw.githubusercontent.com/bbogaert67/ha-ess/main/custom_components/energy_flow_manager/sensor.py -O sensor.py
   ```

5. **Download latest manifest.json**
   ```bash
   wget https://raw.githubusercontent.com/bbogaert67/ha-ess/main/custom_components/energy_flow_manager/manifest.json -O manifest.json
   ```

6. **Download latest __init__.py**
   ```bash
   wget https://raw.githubusercontent.com/bbogaert67/ha-ess/main/custom_components/energy_flow_manager/__init__.py -O __init__.py
   ```

7. **Restart Home Assistant**
   - Settings → System → Restart

### Method 3: Direct File Edit (Quick Fix)

If you can't reinstall, manually edit the file:

1. **Open File Editor** (Settings → Add-ons → File Editor)

2. **Navigate to**: `/config/custom_components/energy_flow_manager/sensor.py`

3. **Find line 171** (around line 171):
   ```python
   "last_update": self.coordinator.last_update_success_time,
   ```
   **Change to**:
   ```python
   "last_update": self.coordinator.last_update_success,
   ```

4. **Find line 230** (around line 230):
   ```python
   "last_update": self.coordinator.last_update_success_time,
   ```
   **Change to**:
   ```python
   "last_update": self.coordinator.last_update_success,
   ```

5. **Save the file**

6. **Restart Home Assistant**

## Verify the Fix Worked

After updating and restarting:

1. **Check Logs** (Settings → System → Logs)
   - Search for "energy_flow_manager"
   - Should see NO AttributeError messages
   - Should see "Energy Flow Manager" loaded successfully

2. **Check Sensors** (Developer Tools → States)
   - Search for "energy_flow_manager"
   - Should see 8 sensors
   - All should have states (not "unavailable")

3. **Test Configuration** (Settings → Devices & Services)
   - Click on "Energy Flow Manager"
   - Click Configure (gear icon)
   - Should open without 500 error
   - Make a small change and save
   - Should work without errors

## Expected Sensors (All 8 Should Work)

After successful update:
- ✅ `sensor.energy_flow_manager_solar_surplus`
- ✅ `sensor.energy_flow_manager_battery_soc`
- ✅ `sensor.energy_flow_manager_battery_power`
- ✅ `sensor.energy_flow_manager_water_temperature`
- ✅ `sensor.energy_flow_manager_available_surplus`
- ✅ `sensor.energy_flow_manager_car_charger_rate`
- ✅ `sensor.energy_flow_manager_water_heater_status`
- ✅ `sensor.energy_flow_manager_car_charger_status`

## Still Getting Errors?

If you still see the AttributeError after following these steps:

1. **Verify file contents**:
   - Open `/config/custom_components/energy_flow_manager/sensor.py`
   - Search for `last_update_success_time`
   - Should find ZERO occurrences
   - Should find `last_update_success` instead

2. **Check manifest version**:
   - Open `/config/custom_components/energy_flow_manager/manifest.json`
   - Should show: `"version": "1.0.7"`

3. **Hard restart**:
   - Stop Home Assistant completely
   - Wait 10 seconds
   - Start Home Assistant
   - Wait for full startup

4. **Check file permissions**:
   ```bash
   ls -la /config/custom_components/energy_flow_manager/
   ```
   - All files should be readable

## About the Commit Hash Display

**This is NORMAL and CORRECT**:
- HACS shows: `cc7013e` (git commit hash)
- Manifest shows: `1.0.7` (version number)
- Both refer to the same code
- The commit hash is how HACS tracks exact versions
- The version number is for human readability

You can verify the version by checking:
```
Settings → Devices & Services → Energy Flow Manager → Information
```

Or by looking at the manifest.json file directly.

## Need More Help?

If none of these methods work:
1. Export your configuration (write down all entity IDs and settings)
2. Completely remove the integration and all files
3. Restart Home Assistant
4. Reinstall fresh from HACS
5. Reconfigure with your saved settings

## Repository Information

- **GitHub**: https://github.com/bbogaert67/ha-ess
- **Latest Commit**: cc7013e
- **Latest Version**: 1.0.7
- **Latest Tag**: v1.0.7
- **Critical Fix**: AttributeError in sensor.py (lines 171 and 230)