#!/bin/bash
# Force reinstall Energy Flow Manager v1.0.19
# This script completely removes and reinstalls the integration

set -e  # Exit on error

echo "========================================="
echo "Energy Flow Manager - Force Reinstall"
echo "Version: 1.0.19"
echo "========================================="
echo ""

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo:"
    echo "sudo bash FORCE_REINSTALL.sh"
    exit 1
fi

# Stop Home Assistant
echo "Step 1: Stopping Home Assistant..."
systemctl stop home-assistant@homeassistant || docker stop homeassistant || echo "Could not stop HA automatically"
sleep 3

# Remove old files
echo "Step 2: Removing old files..."
rm -rf /config/custom_components/energy_flow_manager
rm -rf /config/__pycache__
find /config -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find /config -type f -name "*.pyc" -delete 2>/dev/null || true

# Download v1.0.19
echo "Step 3: Downloading v1.0.19..."
cd /config/custom_components || mkdir -p /config/custom_components && cd /config/custom_components
wget -q https://github.com/bbogaert67/ha-ess/archive/refs/tags/v1.0.19.tar.gz
tar -xzf v1.0.19.tar.gz
mv ha-ess-1.0.19/custom_components/energy_flow_manager .
rm -rf ha-ess-1.0.19 v1.0.19.tar.gz

# Verify installation
echo "Step 4: Verifying installation..."
if [ ! -f "/config/custom_components/energy_flow_manager/__init__.py" ]; then
    echo "ERROR: Installation failed!"
    exit 1
fi

# Check version
VERSION=$(grep "VERSION" /config/custom_components/energy_flow_manager/const.py | cut -d'"' -f2)
echo "Installed version: $VERSION"

# Check for _read_file function
if grep -q "def _read_file" /config/custom_components/energy_flow_manager/__init__.py; then
    echo "✓ Correct code detected (_read_file function found)"
else
    echo "✗ WARNING: _read_file function not found!"
    echo "  This might be the wrong version"
fi

# Check line 96
echo ""
echo "Checking line 96 of __init__.py:"
sed -n '96p' /config/custom_components/energy_flow_manager/__init__.py

# Set permissions
echo ""
echo "Step 5: Setting permissions..."
chown -R homeassistant:homeassistant /config/custom_components/energy_flow_manager 2>/dev/null || true

# Start Home Assistant
echo ""
echo "Step 6: Starting Home Assistant..."
systemctl start home-assistant@homeassistant || docker start homeassistant || echo "Please start HA manually"

echo ""
echo "========================================="
echo "Installation complete!"
echo "========================================="
echo ""
echo "Wait 30 seconds for Home Assistant to start, then check:"
echo "1. Settings → Devices & Services"
echo "2. Look for 'Energy Flow Manager'"
echo "3. Check sidebar for 'Energy Flow' panel"
echo ""
echo "To check logs:"
echo "tail -f /config/home-assistant.log | grep energy_flow_manager"
echo ""

# Made with Bob
