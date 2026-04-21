# Manual Update for Home Assistant OS - v1.0.19

Since you're running Home Assistant OS (HAOS), you need to use the File Editor or Studio Code Server add-on to manually update the files.

## Method 1: Using File Editor Add-on (Easiest)

### Step 1: Install File Editor (if not installed)
1. Settings → Add-ons → Add-on Store
2. Search for "File editor"
3. Install and Start it
4. Go to Configuration tab, enable "Enforce Basepath"

### Step 2: Delete Old Integration
1. Open File Editor
2. Navigate to `config/custom_components/`
3. Delete the entire `energy_flow_manager` folder
4. Settings → System → Restart Home Assistant

### Step 3: Download v1.0.19
1. Go to: https://github.com/bbogaert67/ha-ess/releases/tag/v1.0.19
2. Click "Source code (zip)"
3. Extract the ZIP on your computer
4. Find the `custom_components/energy_flow_manager` folder inside

### Step 4: Upload Files via File Editor
1. In File Editor, navigate to `config/custom_components/`
2. Create new folder: `energy_flow_manager`
3. Upload ALL files from the extracted folder:
   - `__init__.py`
   - `config_flow.py`
   - `const.py`
   - `energy_manager.py`
   - `manifest.json`
   - `panel.html`
   - `panel.py`
   - `sensor.py`
   - `services.yaml`
   - `strings.json`

### Step 5: Verify __init__.py
1. Open `config/custom_components/energy_flow_manager/__init__.py`
2. Scroll to around line 89-96
3. You should see:

```python
def _read_file(file_path: str) -> str:
    """Read file content synchronously (to be called in executor)."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


async def async_register_panel(hass: HomeAssistant) -> None:
    """Register the Energy Flow Manager panel."""
    panel_path = os.path.join(os.path.dirname(__file__), "panel.html")
    
    # Read the panel HTML content asynchronously using executor
    panel_html = await hass.async_add_executor_job(_read_file, panel_path)
```

**If you see this instead (OLD CODE), you have the wrong version:**
```python
    # Read the panel HTML content asynchronously
    panel_html = await hass.async_add_executor_job(
        file_util.read_file, panel_path  # ❌ WRONG!
    )
```

### Step 6: Restart Home Assistant
1. Settings → System → Restart Home Assistant
2. Wait for restart to complete
3. Check Settings → Devices & Services
4. Energy Flow Manager should load without errors

## Method 2: Using Studio Code Server Add-on

### Step 1: Install Studio Code Server
1. Settings → Add-ons → Add-on Store
2. Search for "Studio Code Server"
3. Install and Start it

### Step 2: Open Terminal in Studio Code Server
1. Open Studio Code Server
2. Terminal → New Terminal

### Step 3: Delete Old Files
```bash
cd /config/custom_components
rm -rf energy_flow_manager
```

### Step 4: Download v1.0.19
```bash
cd /config/custom_components
wget https://github.com/bbogaert67/ha-ess/archive/refs/tags/v1.0.19.tar.gz
tar -xzf v1.0.19.tar.gz
mv ha-ess-1.0.19/custom_components/energy_flow_manager .
rm -rf ha-ess-1.0.19 v1.0.19.tar.gz
```

### Step 5: Verify Installation
```bash
# Check version
grep VERSION /config/custom_components/energy_flow_manager/const.py

# Check for _read_file function
grep "def _read_file" /config/custom_components/energy_flow_manager/__init__.py

# View lines 89-100
sed -n '89,100p' /config/custom_components/energy_flow_manager/__init__.py
```

### Step 6: Restart Home Assistant
```bash
ha core restart
```

## Method 3: Via HACS (If Installed)

### Step 1: Remove Integration
1. HACS → Integrations
2. Find "Energy Flow Manager"
3. Click three dots → Remove
4. Confirm removal

### Step 2: Clear Browser Cache
1. Press Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
2. Clear cached images and files
3. Close and reopen browser

### Step 3: Reinstall
1. HACS → Integrations → Explore & Download Repositories
2. Search for "Energy Flow Manager"
3. Download
4. Restart Home Assistant

### Step 4: Verify Version
1. HACS → Integrations → Energy Flow Manager
2. Should show version 1.0.19

## Verification After Update

### Check Logs
Settings → System → Logs

Look for:
- ✅ No "AttributeError: module 'homeassistant.util.file' has no attribute 'read_file'"
- ✅ No "blocking call" warnings
- ✅ "Energy Flow Manager" loads successfully

### Check Integration
1. Settings → Devices & Services
2. Energy Flow Manager should be listed
3. Click on it to see 8 sensors

### Check Panel
1. Look in sidebar for "Energy Flow" (solar icon)
2. Click it
3. Should display all sensor values

## Troubleshooting

### Still Getting Old Error?

The file might not have uploaded correctly. Check:

```bash
# In Studio Code Server terminal
md5sum /config/custom_components/energy_flow_manager/__init__.py
```

Compare with the GitHub version:
```bash
wget -qO- https://raw.githubusercontent.com/bbogaert67/ha-ess/v1.0.19/custom_components/energy_flow_manager/__init__.py | md5sum
```

They should match.

### Panel Still Empty?

1. Hard refresh browser: Ctrl+Shift+R (Cmd+Shift+R on Mac)
2. Clear browser cache completely
3. Try different browser
4. Check browser console (F12) for errors

### Integration Won't Load?

1. Check all files are present:
```bash
ls -la /config/custom_components/energy_flow_manager/
```

Should show all 10 files.

2. Check file permissions:
```bash
ls -l /config/custom_components/energy_flow_manager/__init__.py
```

Should be readable.

3. Check for syntax errors:
```bash
python3 -m py_compile /config/custom_components/energy_flow_manager/__init__.py
```

Should complete without errors.

## Need Help?

If you're still having issues:

1. Share the output of:
```bash
sed -n '89,100p' /config/custom_components/energy_flow_manager/__init__.py
```

2. Share the full error from logs

3. Confirm which method you used to update

## Important Notes for HAOS

- ❌ Cannot use bash scripts directly
- ❌ Cannot use `sudo` commands
- ✅ Must use File Editor or Studio Code Server
- ✅ Must use HACS or manual file upload
- ✅ Terminal commands only work in Studio Code Server add-on