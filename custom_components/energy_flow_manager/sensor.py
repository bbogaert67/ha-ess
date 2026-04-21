"""Sensor platform for Energy Flow Manager."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfPower,
    UnitOfTemperature,
    PERCENTAGE,
    UnitOfElectricCurrent,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    DOMAIN,
    ATTR_SOLAR_SURPLUS,
    ATTR_BATTERY_SOC,
    ATTR_BATTERY_POWER,
    ATTR_WATER_TEMP,
    ATTR_WATER_HEATER_STATUS,
    ATTR_CAR_CHARGER_STATUS,
    ATTR_CAR_CHARGER_RATE,
    ATTR_AVAILABLE_SURPLUS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Energy Flow Manager sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    manager = hass.data[DOMAIN][entry.entry_id]["manager"]

    sensors = [
        EnergyFlowSensor(
            coordinator,
            entry,
            "Solar Surplus",
            ATTR_SOLAR_SURPLUS,
            UnitOfPower.WATT,
            SensorDeviceClass.POWER,
            SensorStateClass.MEASUREMENT,
        ),
        EnergyFlowSensor(
            coordinator,
            entry,
            "Battery SOC",
            ATTR_BATTERY_SOC,
            PERCENTAGE,
            SensorDeviceClass.BATTERY,
            SensorStateClass.MEASUREMENT,
        ),
        EnergyFlowSensor(
            coordinator,
            entry,
            "Battery Power",
            ATTR_BATTERY_POWER,
            UnitOfPower.WATT,
            SensorDeviceClass.POWER,
            SensorStateClass.MEASUREMENT,
        ),
        EnergyFlowSensor(
            coordinator,
            entry,
            "Water Temperature",
            ATTR_WATER_TEMP,
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
        ),
        EnergyFlowSensor(
            coordinator,
            entry,
            "Available Surplus",
            ATTR_AVAILABLE_SURPLUS,
            UnitOfPower.WATT,
            SensorDeviceClass.POWER,
            SensorStateClass.MEASUREMENT,
        ),
        EnergyFlowSensor(
            coordinator,
            entry,
            "Car Charger Rate",
            ATTR_CAR_CHARGER_RATE,
            UnitOfElectricCurrent.AMPERE,
            SensorDeviceClass.CURRENT,
            SensorStateClass.MEASUREMENT,
        ),
        EnergyFlowStatusSensor(
            coordinator,
            entry,
            "Water Heater Status",
            ATTR_WATER_HEATER_STATUS,
        ),
        EnergyFlowStatusSensor(
            coordinator,
            entry,
            "Car Charger Status",
            ATTR_CAR_CHARGER_STATUS,
        ),
    ]

    async_add_entities(sensors)


class EnergyFlowSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Energy Flow Manager sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        name: str,
        data_key: str,
        unit: str | None,
        device_class: SensorDeviceClass | None,
        state_class: SensorStateClass | None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._name = name
        self._data_key = data_key
        self._attr_name = f"Energy Flow Manager {name}"
        self._attr_unique_id = f"{entry.entry_id}_{data_key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "Energy Flow Manager",
            "manufacturer": "Custom",
            "model": "Energy Flow Manager",
            "sw_version": "1.0.0",
        }

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get(self._data_key)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}
        
        return {
            "last_update": self.coordinator.last_update_success,
        }


class EnergyFlowStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Energy Flow Manager status sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        name: str,
        data_key: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._name = name
        self._data_key = data_key
        self._attr_name = f"Energy Flow Manager {name}"
        self._attr_unique_id = f"{entry.entry_id}_{data_key}"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "Energy Flow Manager",
            "manufacturer": "Custom",
            "model": "Energy Flow Manager",
            "sw_version": "1.0.0",
        }

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        if self.coordinator.data:
            is_active = self.coordinator.data.get(self._data_key, False)
            return "on" if is_active else "off"
        return "unknown"

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        if self.coordinator.data:
            is_active = self.coordinator.data.get(self._data_key, False)
            if "water" in self._data_key.lower():
                return "mdi:water-boiler" if is_active else "mdi:water-boiler-off"
            elif "car" in self._data_key.lower():
                return "mdi:ev-station" if is_active else "mdi:ev-station"
        return "mdi:help-circle"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}
        
        return {
            "last_update": self.coordinator.last_update_success,
        }

# Made with Bob
