# Clear Python Cache and Force Reload - v1.0.18

## Problem
After updating to v1.0.18, you're still seeing the blocking I/O error with the old code at line 94.

## Root Cause
Home Assistant is running cached Python bytecode (`.pyc` files) from the previous version instead of the new code.

## Solution: Complete Cache Clear

### Step 1: Stop Home Assistant
```bash
# If running as a service
sudo systemctl stop home-assistant@homeassistant

# Or if running in Docker
docker stop homeassistant

# Or from Home Assistant UI
Settings → System → Restart Home Assistant → Stop
```

### Step 2: Delete ALL Cache Files
```bash
# Navigate to custom components directory
cd /config/custom_components/energy_flow_manager

# Delete all Python cache files
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

# Also clear Home Assistant's main cache
rm -rf /config/__pycache__
rm -rf /config/.storage/__pycache__
```

### Step 3: Verify New Code is Present
```bash
# Check line 94-96 in __init__.py
sed -n '94,96p' /config/custom_components/energy_flow_manager/__init__.py
```

**Expected output:**
```python
    # Read the panel HTML content asynchronously
    panel_html = await hass.async_add_executor_job(
        file_util.read_file, panel_path
```

**If you see this instead (OLD CODE):**
```python
    with open(panel_path, "r", encoding="utf-8") as file:
        panel_html = file.read()
```

Then you need to re-download v1.0.18 from GitHub.

### Step 4: Re-download v1.0.18 (if needed)
```bash
# Remove old files
rm -rf /config/custom_components/energy_flow_manager

# Download latest version
cd /config/custom_components
wget https://github.com/bbogaert67/ha-ess/archive/refs/tags/v1.0.18.zip
unzip v1.0.18.zip
mv ha-ess-1.0.18/custom_components/energy_flow_manager .
rm -rf ha-ess-1.0.18 v1.0.18.zip
```

### Step 5: Start Home Assistant
```bash
# If running as a service
sudo systemctl start home-assistant@homeassistant

# Or if running in Docker
docker start homeassistant

# Or from Home Assistant UI
Settings → System → Restart Home Assistant
```

### Step 6: Verify Fix
Check the Home Assistant logs:
```bash
tail -f /config/home-assistant.log | grep "blocking call"
```

You should NOT see any blocking call warnings for energy_flow_manager.

## Alternative: Nuclear Option

If the above doesn't work, completely remove and reinstall:

```bash
# 1. Stop Home Assistant
sudo systemctl stop home-assistant@homeassistant

# 2. Remove integration from UI
# (Skip this step, we'll do it manually)

# 3. Delete ALL related files
rm -rf /config/custom_components/energy_flow_manager
rm -rf /config/.storage/core.config_entries  # WARNING: This removes ALL integrations!
rm -rf /config/__pycache__

# 4. Download fresh copy
cd /config/custom_components
git clone https://github.com/bbogaert67/ha-ess.git temp
mv temp/custom_components/energy_flow_manager .
rm -rf temp

# 5. Start Home Assistant
sudo systemctl start home-assistant@homeassistant

# 6. Re-add integration via UI
# Settings → Devices & Services → Add Integration → Energy Flow Manager
```

## Verification Commands

### Check Python Cache
```bash
find /config/custom_components/energy_flow_manager -name "*.pyc" -o -name "__pycache__"
```
Should return nothing.

### Check Code Version
```bash
grep "VERSION" /config/custom_components/energy_flow_manager/const.py
```
Should show: `VERSION = "1.0.18"`

### Check Async File Reading
```bash
grep -A 2 "async_add_executor_job" /config/custom_components/energy_flow_manager/__init__.py
```
Should show the async file reading code.

## Still Having Issues?

1. Check you're editing the correct file location
2. Verify file permissions: `ls -la /config/custom_components/energy_flow_manager/`
3. Check Home Assistant is actually restarting (not just reloading)
4. Look for any file system errors in logs
5. Try the "Nuclear Option" above

## Why This Happens

Python caches compiled bytecode in `__pycache__` directories and `.pyc` files for performance. When you update code, Python may continue using the cached version unless:
- The cache is explicitly cleared
- The modification time of the source file is newer than the cache
- Python is completely restarted (not just reloaded)

Home Assistant's reload functionality doesn't always clear Python's bytecode cache, especially for custom components.