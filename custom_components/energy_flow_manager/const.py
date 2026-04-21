"""Constants for the Energy Flow Manager integration."""

DOMAIN = "energy_flow_manager"
VERSION = "1.0.12"

# Configuration keys
CONF_SOLAR_SURPLUS_SENSOR = "solar_surplus_sensor"
CONF_BATTERY_SOC_SENSOR = "battery_soc_sensor"
CONF_BATTERY_POWER_SENSOR = "battery_power_sensor"
CONF_WATER_TEMP_SENSOR = "water_temp_sensor"
CONF_WATER_HEATER_SWITCH = "water_heater_switch"
CONF_CAR_CHARGER_SWITCH = "car_charger_switch"

# Water heater configuration
CONF_WATER_HEATER_ENABLED = "water_heater_enabled"
CONF_WATER_HEATER_MIN_SURPLUS = "water_heater_min_surplus"
CONF_WATER_HEATER_MIN_TEMP = "water_heater_min_temp"
CONF_WATER_HEATER_MAX_TEMP = "water_heater_max_temp"
CONF_WATER_HEATER_POWER = "water_heater_power"

# Car charger configuration
CONF_CAR_CHARGER_ENABLED = "car_charger_enabled"
CONF_CAR_CHARGER_MIN_SURPLUS = "car_charger_min_surplus"
CONF_CAR_CHARGER_MIN_RATE = "car_charger_min_rate"
CONF_CAR_CHARGER_MAX_RATE = "car_charger_max_rate"
CONF_CAR_CHARGER_RATE_ENTITY = "car_charger_rate_entity"

# Battery configuration
CONF_BATTERY_MIN_SOC = "battery_min_soc"
CONF_BATTERY_MAX_SOC = "battery_max_soc"

# Update interval
CONF_UPDATE_INTERVAL = "update_interval"

# Default values
DEFAULT_WATER_HEATER_MIN_SURPLUS = 2000  # Watts
DEFAULT_WATER_HEATER_MIN_TEMP = 40  # Celsius
DEFAULT_WATER_HEATER_MAX_TEMP = 60  # Celsius
DEFAULT_WATER_HEATER_POWER = 2000  # Watts

DEFAULT_CAR_CHARGER_MIN_SURPLUS = 1400  # Watts (minimum 6A at 230V)
DEFAULT_CAR_CHARGER_MIN_RATE = 6  # Amperes
DEFAULT_CAR_CHARGER_MAX_RATE = 16  # Amperes

DEFAULT_BATTERY_MIN_SOC = 20  # Percent
DEFAULT_BATTERY_MAX_SOC = 90  # Percent

DEFAULT_UPDATE_INTERVAL = 30  # Seconds

# Sensor attributes
ATTR_SOLAR_SURPLUS = "solar_surplus"
ATTR_BATTERY_SOC = "battery_soc"
ATTR_BATTERY_POWER = "battery_power"
ATTR_WATER_TEMP = "water_temp"
ATTR_WATER_HEATER_STATUS = "water_heater_status"
ATTR_CAR_CHARGER_STATUS = "car_charger_status"
ATTR_CAR_CHARGER_RATE = "car_charger_rate"
ATTR_AVAILABLE_SURPLUS = "available_surplus"

# Service names
SERVICE_UPDATE_CONFIG = "update_config"
SERVICE_FORCE_UPDATE = "force_update"

# Made with Bob
