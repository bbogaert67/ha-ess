# HACS Installation Troubleshooting

## Issue: "The version 6d745ab for this integration can not be used with HACS"

This error occurs when HACS is referencing an old commit instead of the proper version tag.

## Solution Steps:

### Step 1: Remove the Integration from HACS (if already added)

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Find "Energy Flow Manager" (if it exists)
4. Click on it
5. Click the **three dots** (⋮) menu
6. Select **Remove**
7. Confirm removal

### Step 2: Clear HACS Cache

1. Go to **Settings** → **System** → **Repairs**
2. Look for any HACS-related issues and resolve them
3. Or restart Home Assistant to clear cache

### Step 3: Re-add the Repository

1. Open HACS → **Integrations**
2. Click **⋮** (three dots) → **Custom repositories**
3. If the repository already exists, **remove it first**
4. Add it fresh:
   - **Repository**: `https://github.com/bbogaert67/ha-ess`
   - **Category**: `Integration`
5. Click **Add**

### Step 4: Wait for HACS to Refresh

HACS needs to fetch the latest repository information:
- This can take a few minutes
- HACS will automatically detect the v1.0.0 tag

### Step 5: Install the Integration

1. Click **+ EXPLORE & DOWNLOAD REPOSITORIES**
2. Search for "Energy Flow Manager"
3. Click on it
4. Click **Download**
5. Select version **v1.0.0** (should be the default)
6. Click **Download**
7. Restart Home Assistant

## Alternative: Manual Installation (Bypass HACS)

If HACS continues to have issues, install manually:

### Method 1: Download Release

1. Go to: https://github.com/bbogaert67/ha-ess/releases/tag/v1.0.0
2. Download the source code (zip or tar.gz)
3. Extract the archive
4. Copy `custom_components/energy_flow_manager` to your Home Assistant config directory
5. Restart Home Assistant

### Method 2: Git Clone

```bash
cd /config/custom_components
git clone https://github.com/bbogaert67/ha-ess.git temp
mv temp/custom_components/energy_flow_manager ./
rm -rf temp
```

Then restart Home Assistant.

## Verify Installation

After installation (via HACS or manual):

1. Check that files exist:
   ```
   /config/custom_components/energy_flow_manager/
   ├── __init__.py
   ├── config_flow.py
   ├── const.py
   ├── energy_manager.py
   ├── manifest.json
   ├── sensor.py
   ├── services.yaml
   └── strings.json
   ```

2. Check Home Assistant logs for errors:
   - Go to **Settings** → **System** → **Logs**
   - Look for "energy_flow_manager" entries

3. Add the integration:
   - **Settings** → **Devices & Services**
   - **+ ADD INTEGRATION**
   - Search "Energy Flow Manager"

## Why This Happened

The initial commit (6d745ab) didn't have a version tag. HACS requires proper semantic versioning (v1.0.0, v1.0.1, etc.) to work correctly.

**What was fixed:**
- ✅ Added `hacs.json` configuration
- ✅ Created version tag `v1.0.0`
- ✅ Tag points to commit `bfb76be` which includes HACS compatibility

## Current Repository Status

- **Latest Commit**: fb9c72a (Add HACS installation guide)
- **Version Tag**: v1.0.0 (points to commit bfb76be)
- **HACS Compatible**: ✅ Yes
- **GitHub**: https://github.com/bbogaert67/ha-ess

## Still Having Issues?

1. **Check GitHub**: Verify the tag exists at https://github.com/bbogaert67/ha-ess/tags
2. **Check Release**: Verify the release at https://github.com/bbogaert67/ha-ess/releases
3. **HACS Version**: Make sure you're running the latest HACS version
4. **Home Assistant Version**: Requires HA 2023.1.0 or newer

## Contact

If you continue to experience issues:
1. Open an issue: https://github.com/bbogaert67/ha-ess/issues
2. Include:
   - Home Assistant version
   - HACS version
   - Full error message
   - Installation method attempted