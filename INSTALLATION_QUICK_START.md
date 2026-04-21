# Energy Flow Manager - Quick Start Guide

## 🚀 Installation in 3 Steps

### Step 1: Copy Files
Copy the `custom_components/energy_flow_manager` folder to your Home Assistant `config/custom_components/` directory.

```
/config/
  └── custom_components/
      └── energy_flow_manager/
          ├── __init__.py
          ├── config_flow.py
          ├── const.py
          ├── energy_manager.py
          ├── manifest.json
          ├── sensor.py
          ├── services.yaml
          └── strings.json
```

### Step 2: Restart Home Assistant
Restart Home Assistant to load the new integration.

### Step 3: Add Integration via UI
Go to **Settings** → **Devices & Services** → **Add Integration** → Search "Energy Flow Manager"

---

## 📋 Configuration Wizard (4 Easy Steps)

### Step 1️⃣: Select Input Sensors

**What you need:**
- ✅ Solar surplus sensor (REQUIRED)
- ⚡ Battery SOC sensor (optional)
- 🔋 Battery power sensor (optional)
- 🌡️ Water temperature sensor (optional)

**UI Form:**
```
┌──────────────────────────────────────────┐
│ Solar Surplus Sensor *                   │
│ [Select sensor.solar_surplus        ▼]  │
│                                          │
│ Battery SOC Sensor                       │
│ [Select sensor.battery_soc          ▼]  │
│                                          │
│ Battery Power Sensor                     │
│ [Select sensor.battery_power        ▼]  │
│                                          │
│ Water Temperature Sensor                 │
│ [Select sensor.water_temp           ▼]  │
│                                          │
│                    [Cancel]  [Submit]    │
└──────────────────────────────────────────┘
```

---

### Step 2️⃣: Configure Water Heater

**What you need:**
- 🔌 Water heater switch entity
- ⚙️ Power consumption (Watts)
- 🌡️ Temperature thresholds

**UI Form:**
```
┌──────────────────────────────────────────┐
│ Water Heater Switch                      │
│ [Select switch.water_heater         ▼]  │
│                                          │
│ Min Surplus to Heat (W)                  │
│ [2000                              ▲▼]  │
│                                          │
│ Min Temperature (°C)                     │
│ [40                                ▲▼]  │
│                                          │
│ Max Temperature (°C)                     │
│ [60                                ▲▼]  │
│                                          │
│ Heater Power (W)                         │
│ [2000                              ▲▼]  │
│                                          │
│                    [Cancel]  [Submit]    │
└──────────────────────────────────────────┘
```

**Defaults:**
- Min Surplus: 2000W
- Min Temp: 40°C
- Max Temp: 60°C
- Power: 2000W

---

### Step 3️⃣: Configure Car Charger

**What you need:**
- 🚗 Car charger switch entity
- 🔢 Charge rate control entity (optional)
- ⚡ Min/Max charge rates (Amperes)

**UI Form:**
```
┌──────────────────────────────────────────┐
│ Car Charger Switch                       │
│ [Select switch.car_charger          ▼]  │
│                                          │
│ Charge Rate Control                      │
│ [Select number.charger_current      ▼]  │
│                                          │
│ Min Surplus to Charge (W)                │
│ [1400                              ▲▼]  │
│                                          │
│ Min Charge Rate (A)                      │
│ [6                                 ▲▼]  │
│                                          │
│ Max Charge Rate (A)                      │
│ [16                                ▲▼]  │
│                                          │
│                    [Cancel]  [Submit]    │
└──────────────────────────────────────────┘
```

**Defaults:**
- Min Surplus: 1400W (6A × 230V)
- Min Rate: 6A
- Max Rate: 16A

---

### Step 4️⃣: Battery & General Settings

**What you configure:**
- 🔋 Battery protection thresholds
- ⏱️ Update frequency

**UI Form:**
```
┌──────────────────────────────────────────┐
│ Min Battery SOC (%)                      │
│ [20                                ▲▼]  │
│                                          │
│ Max Battery SOC (%)                      │
│ [90                                ▲▼]  │
│                                          │
│ Update Interval (seconds)                │
│ [30                                ▲▼]  │
│                                          │
│                    [Cancel]  [Submit]    │
└──────────────────────────────────────────┘
```

**Defaults:**
- Min SOC: 20%
- Max SOC: 90%
- Update: 30 seconds

---

## ✅ What You Get After Configuration

### 8 New Sensors:
1. 🌞 `sensor.energy_flow_manager_solar_surplus` - Current surplus (W)
2. 🔋 `sensor.energy_flow_manager_battery_soc` - Battery level (%)
3. ⚡ `sensor.energy_flow_manager_battery_power` - Battery flow (W)
4. 🌡️ `sensor.energy_flow_manager_water_temperature` - Water temp (°C)
5. 📊 `sensor.energy_flow_manager_available_surplus` - Available power (W)
6. 🚗 `sensor.energy_flow_manager_car_charger_rate` - Charge rate (A)
7. 💧 `sensor.energy_flow_manager_water_heater_status` - Heater state
8. 🔌 `sensor.energy_flow_manager_car_charger_status` - Charger state

### 1 New Service:
- `energy_flow_manager.force_update` - Manual update trigger

---

## 🎯 Quick Configuration Examples

### Example 1: Basic Solar + Water Heater
```
Step 1: sensor.solar_surplus
Step 2: switch.water_heater, 2000W, 40-60°C
Step 3: (skip)
Step 4: 20% SOC, 30s update
```

### Example 2: Full System with EV
```
Step 1: sensor.solar_surplus, sensor.battery_soc
Step 2: switch.water_heater, 2000W, 40-60°C
Step 3: switch.car_charger, number.charger_current, 6-16A
Step 4: 20% SOC, 30s update
```

### Example 3: EV Only (No Water Heater)
```
Step 1: sensor.solar_surplus, sensor.battery_soc
Step 2: (skip - leave all empty)
Step 3: switch.car_charger, number.charger_current, 6-16A
Step 4: 20% SOC, 30s update
```

---

## 🔧 Reconfiguration

Need to change settings? Easy!

1. Go to **Settings** → **Devices & Services**
2. Find "Energy Flow Manager"
3. Click **⋮** (three dots)
4. Select **Configure**
5. Update any values
6. Click **Submit**

---

## 📱 Add to Dashboard

Quick Lovelace card:

```yaml
type: entities
title: Energy Flow Manager
entities:
  - sensor.energy_flow_manager_solar_surplus
  - sensor.energy_flow_manager_battery_soc
  - sensor.energy_flow_manager_water_heater_status
  - sensor.energy_flow_manager_car_charger_status
  - sensor.energy_flow_manager_car_charger_rate
```

---

## 🆘 Troubleshooting

### Integration not showing up?
- ✅ Check files are in `config/custom_components/energy_flow_manager/`
- ✅ Restart Home Assistant
- ✅ Check logs for errors

### Entities not found?
- ✅ Verify entity IDs in **Developer Tools** → **States**
- ✅ Make sure sensors are working (check their values)
- ✅ Use the dropdown selector to find entities

### Devices not turning on?
- ✅ Check solar surplus is above threshold
- ✅ Verify battery SOC is above minimum
- ✅ Test switches manually first
- ✅ Check Home Assistant logs

---

## 📚 More Information

- **Full Documentation**: See `README.md`
- **UI Guide**: See `UI_CONFIGURATION_GUIDE.md`
- **Examples**: See `example_configuration.yaml`

---

## 🎉 You're Done!

The integration will now:
- ✅ Monitor your solar surplus
- ✅ Protect your battery
- ✅ Heat water when surplus is available
- ✅ Charge your car dynamically
- ✅ Prioritize water heater over car charging
- ✅ Update every 30 seconds (or your configured interval)

Enjoy your optimized energy management! 🌞🔋⚡