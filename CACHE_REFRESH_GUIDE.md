# Home Assistant Cache Refresh Guide

## Problem
Home Assistant information page shows old commit hash `e979e5b` instead of the latest `dbd50bc` (v1.0.4).

## Why This Happens
Home Assistant caches integration information to improve performance. When you update an integration via HACS or manually, the cache may not refresh immediately.

## Solution Methods

### Method 1: Force HACS to Redownload (Recommended)
1. Open Home Assistant
2. Go to **HACS** → **Integrations**
3. Find **Energy Flow Manager**
4. Click the **three dots menu** (⋮)
5. Select **Redownload**
6. Wait for download to complete
7. Go to **Settings** → **System** → **Restart Home Assistant**
8. After restart, check the information page

### Method 2: Clear HACS Cache
1. Go to **Settings** → **System** → **Restart Home Assistant**
2. After restart, go to **HACS** → **Integrations**
3. Click **Energy Flow Manager**
4. The information should now show the latest commit

### Method 3: Remove and Reinstall Integration
1. Go to **HACS** → **Integrations**
2. Find **Energy Flow Manager**
3. Click the **three dots menu** (⋮)
4. Select **Remove**
5. Confirm removal
6. Go to **HACS** → **Integrations** → **Explore & Download Repositories**
7. Search for **Energy Flow Manager**
8. Click **Download**
9. Restart Home Assistant
10. Reconfigure the integration

### Method 4: Manual Cache Clear (Advanced)
1. Stop Home Assistant
2. Delete the HACS cache directory:
   ```bash
   rm -rf /config/.storage/hacs*
   ```
3. Start Home Assistant
4. HACS will rebuild its cache with the latest information

### Method 5: Force Update via HACS API (Advanced)
1. Go to **Developer Tools** → **Services**
2. Call service: `hacs.repository_update`
3. Service data:
   ```yaml
   repository: bbogaert67/ha-ess
   ```
4. Restart Home Assistant

## Verification
After applying any method, verify the update:

1. Go to **HACS** → **Integrations** → **Energy Flow Manager**
2. Check the **Information** tab
3. Verify it shows commit hash: `dbd50bc`
4. Verify version shows: `1.0.4`

## Current Repository Status
- **Repository**: https://github.com/bbogaert67/ha-ess
- **Latest Commit**: `dbd50bc` (Bump version to 1.0.4)
- **Latest Version**: v1.0.4
- **Latest Tag**: v1.0.4

## What Changed in v1.0.4
- Added enable/disable switches for water heater control
- Added enable/disable switches for car charger control
- Both controls are enabled by default
- Can be toggled in configuration UI without losing other settings

## Notes
- The old commit hash `e979e5b` is from an earlier version
- The integration functionality is not affected by the cached information
- The cache only affects the displayed information in HACS
- Your integration is running the correct version if you've restarted Home Assistant after the update