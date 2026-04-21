# Installing Energy Flow Manager via HACS

## ✅ HACS Compatibility Added

The repository now includes:
- ✅ `hacs.json` configuration file
- ✅ Version tag `v1.0.0`
- ✅ Proper repository structure

## Installation Methods

### Method 1: Add as Custom Repository (Recommended)

1. **Open HACS** in Home Assistant
2. Click on **Integrations**
3. Click the **three dots** (⋮) in the top right corner
4. Select **Custom repositories**
5. Add the repository:
   - **Repository**: `https://github.com/bbogaert67/ha-ess`
   - **Category**: `Integration`
6. Click **Add**
7. Click **+ EXPLORE & DOWNLOAD REPOSITORIES**
8. Search for "Energy Flow Manager"
9. Click **Download**
10. Restart Home Assistant

### Method 2: Manual Installation

1. Download the latest release from: https://github.com/bbogaert67/ha-ess/releases
2. Extract the `custom_components/energy_flow_manager` folder
3. Copy it to your Home Assistant `config/custom_components/` directory
4. Restart Home Assistant

## After Installation

1. Go to **Settings** → **Devices & Services**
2. Click **+ ADD INTEGRATION**
3. Search for "Energy Flow Manager"
4. Follow the 4-step configuration wizard

## Version Information

- **Current Version**: v1.0.0
- **Minimum Home Assistant Version**: 2023.1.0
- **HACS Compatible**: ✅ Yes

## Troubleshooting HACS Installation

### "Repository structure is not compliant"
- ✅ Fixed: Repository now has proper structure with `hacs.json`

### "No version found"
- ✅ Fixed: Version tag `v1.0.0` has been created

### "Integration not found after installation"
- Restart Home Assistant
- Check that files are in `config/custom_components/energy_flow_manager/`
- Check Home Assistant logs for errors

### "Version 6d745ab cannot be used with HACS"
- ✅ Fixed: Proper version tag created
- Update HACS to use the new v1.0.0 release

## Repository Information

- **GitHub**: https://github.com/bbogaert67/ha-ess
- **Latest Release**: https://github.com/bbogaert67/ha-ess/releases/latest
- **Issues**: https://github.com/bbogaert67/ha-ess/issues

## What's Included

- Full UI configuration (no YAML editing!)
- 4-step configuration wizard
- 8 monitoring sensors
- Smart energy flow management
- Water heater control
- EV charger control with dynamic rate adjustment
- Battery protection
- Comprehensive documentation

## Support

For issues or questions:
1. Check the [README.md](README.md) for documentation
2. Review [UI_CONFIGURATION_GUIDE.md](UI_CONFIGURATION_GUIDE.md) for setup help
3. Open an issue on GitHub if you need assistance