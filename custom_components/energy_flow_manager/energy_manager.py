"""Energy Flow Manager core logic."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers import entity_registry as er
from homeassistant.const import STATE_ON, STATE_OFF, STATE_UNAVAILABLE, STATE_UNKNOWN

from .const import (
    CONF_SOLAR_SURPLUS_SENSOR,
    CONF_BATTERY_SOC_SENSOR,
    CONF_BATTERY_POWER_SENSOR,
    CONF_WATER_TEMP_SENSOR,
    CONF_WATER_HEATER_SWITCH,
    CONF_CAR_CHARGER_SWITCH,
    CONF_WATER_HEATER_MIN_SURPLUS,
    CONF_WATER_HEATER_MIN_TEMP,
    CONF_WATER_HEATER_MAX_TEMP,
    CONF_WATER_HEATER_POWER,
    CONF_CAR_CHARGER_MIN_SURPLUS,
    CONF_CAR_CHARGER_MIN_RATE,
    CONF_CAR_CHARGER_MAX_RATE,
    CONF_CAR_CHARGER_RATE_ENTITY,
    CONF_BATTERY_MIN_SOC,
    CONF_BATTERY_MAX_SOC,
    DEFAULT_WATER_HEATER_MIN_SURPLUS,
    DEFAULT_WATER_HEATER_MIN_TEMP,
    DEFAULT_WATER_HEATER_MAX_TEMP,
    DEFAULT_WATER_HEATER_POWER,
    DEFAULT_CAR_CHARGER_MIN_SURPLUS,
    DEFAULT_CAR_CHARGER_MIN_RATE,
    DEFAULT_CAR_CHARGER_MAX_RATE,
    DEFAULT_BATTERY_MIN_SOC,
    DEFAULT_BATTERY_MAX_SOC,
)

_LOGGER = logging.getLogger(__name__)


class EnergyFlowManager:
    """Manage energy flows and device control."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the energy flow manager."""
        self.hass = hass
        self.entry = entry
        self._data: dict[str, Any] = {}
        
    @property
    def config(self) -> dict[str, Any]:
        """Return the configuration."""
        return self.entry.data

    def _get_state_value(self, entity_id: str | None) -> float | None:
        """Get numeric state value from entity."""
        if not entity_id:
            return None
            
        state = self.hass.states.get(entity_id)
        if not state or state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            return None
            
        try:
            return float(state.state)
        except (ValueError, TypeError):
            _LOGGER.warning("Could not convert state of %s to float: %s", entity_id, state.state)
            return None

    def _get_boolean_state(self, entity_id: str | None) -> bool:
        """Get boolean state from entity."""
        if not entity_id:
            return False
            
        state = self.hass.states.get(entity_id)
        if not state or state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            return False
            
        return state.state == STATE_ON

    async def async_update(self) -> dict[str, Any]:
        """Update energy flow data and control devices."""
        # Get current sensor values
        solar_surplus = self._get_state_value(self.config.get(CONF_SOLAR_SURPLUS_SENSOR))
        battery_soc = self._get_state_value(self.config.get(CONF_BATTERY_SOC_SENSOR))
        battery_power = self._get_state_value(self.config.get(CONF_BATTERY_POWER_SENSOR))
        water_temp = self._get_state_value(self.config.get(CONF_WATER_TEMP_SENSOR))

        # Store current values
        self._data = {
            "solar_surplus": solar_surplus,
            "battery_soc": battery_soc,
            "battery_power": battery_power,
            "water_temp": water_temp,
            "water_heater_active": False,
            "car_charger_active": False,
            "car_charger_rate": 0,
            "available_surplus": solar_surplus or 0,
        }

        # Control devices based on energy availability
        await self._control_water_heater(solar_surplus, battery_soc, water_temp)
        await self._control_car_charger(solar_surplus, battery_soc)

        return self._data

    async def _control_water_heater(
        self, 
        solar_surplus: float | None, 
        battery_soc: float | None,
        water_temp: float | None
    ) -> None:
        """Control water heater based on surplus energy and temperature."""
        water_heater_switch = self.config.get(CONF_WATER_HEATER_SWITCH)
        if not water_heater_switch:
            return

        # Get configuration
        min_surplus = self.config.get(CONF_WATER_HEATER_MIN_SURPLUS, DEFAULT_WATER_HEATER_MIN_SURPLUS)
        min_temp = self.config.get(CONF_WATER_HEATER_MIN_TEMP, DEFAULT_WATER_HEATER_MIN_TEMP)
        max_temp = self.config.get(CONF_WATER_HEATER_MAX_TEMP, DEFAULT_WATER_HEATER_MAX_TEMP)
        heater_power = self.config.get(CONF_WATER_HEATER_POWER, DEFAULT_WATER_HEATER_POWER)
        min_battery_soc = self.config.get(CONF_BATTERY_MIN_SOC, DEFAULT_BATTERY_MIN_SOC)

        # Check if we should turn on/off the water heater
        should_heat = False
        
        if solar_surplus is not None and water_temp is not None:
            # Check battery SOC if configured
            battery_ok = True
            if battery_soc is not None:
                battery_ok = battery_soc >= min_battery_soc

            # Turn on if: enough surplus, battery OK, and temp below max
            if solar_surplus >= min_surplus and battery_ok and water_temp < max_temp:
                should_heat = True
                self._data["available_surplus"] -= heater_power
            # Turn off if: temp reached max or not enough surplus
            elif water_temp >= max_temp or solar_surplus < min_surplus:
                should_heat = False

        # Get current state
        current_state = self._get_boolean_state(water_heater_switch)

        # Control the switch
        if should_heat and not current_state:
            await self.hass.services.async_call(
                "switch", "turn_on", {"entity_id": water_heater_switch}
            )
            _LOGGER.info("Turned on water heater (surplus: %s W, temp: %s°C)", solar_surplus, water_temp)
        elif not should_heat and current_state:
            await self.hass.services.async_call(
                "switch", "turn_off", {"entity_id": water_heater_switch}
            )
            _LOGGER.info("Turned off water heater (surplus: %s W, temp: %s°C)", solar_surplus, water_temp)

        self._data["water_heater_active"] = should_heat

    async def _control_car_charger(
        self, 
        solar_surplus: float | None, 
        battery_soc: float | None
    ) -> None:
        """Control car charger based on surplus energy."""
        car_charger_switch = self.config.get(CONF_CAR_CHARGER_SWITCH)
        if not car_charger_switch:
            return

        # Get configuration
        min_surplus = self.config.get(CONF_CAR_CHARGER_MIN_SURPLUS, DEFAULT_CAR_CHARGER_MIN_SURPLUS)
        min_rate = self.config.get(CONF_CAR_CHARGER_MIN_RATE, DEFAULT_CAR_CHARGER_MIN_RATE)
        max_rate = self.config.get(CONF_CAR_CHARGER_MAX_RATE, DEFAULT_CAR_CHARGER_MAX_RATE)
        rate_entity = self.config.get(CONF_CAR_CHARGER_RATE_ENTITY)
        min_battery_soc = self.config.get(CONF_BATTERY_MIN_SOC, DEFAULT_BATTERY_MIN_SOC)

        # Check if we should charge
        should_charge = False
        charge_rate = 0

        if solar_surplus is not None:
            # Check battery SOC if configured
            battery_ok = True
            if battery_soc is not None:
                battery_ok = battery_soc >= min_battery_soc

            # Calculate available surplus (after water heater)
            available = self._data.get("available_surplus", solar_surplus)

            if available >= min_surplus and battery_ok:
                should_charge = True
                # Calculate optimal charge rate based on available surplus
                # Assuming 230V single phase: Power = Voltage * Current
                voltage = 230
                max_power = max_rate * voltage
                min_power = min_rate * voltage
                
                if available >= max_power:
                    charge_rate = max_rate
                elif available >= min_power:
                    # Scale linearly between min and max rate
                    charge_rate = min_rate + (available - min_power) / (max_power - min_power) * (max_rate - min_rate)
                    charge_rate = round(charge_rate, 1)
                else:
                    should_charge = False

        # Get current state
        current_state = self._get_boolean_state(car_charger_switch)

        # Control the charger
        if should_charge and not current_state:
            await self.hass.services.async_call(
                "switch", "turn_on", {"entity_id": car_charger_switch}
            )
            _LOGGER.info("Turned on car charger (surplus: %s W, rate: %s A)", solar_surplus, charge_rate)
        elif not should_charge and current_state:
            await self.hass.services.async_call(
                "switch", "turn_off", {"entity_id": car_charger_switch}
            )
            _LOGGER.info("Turned off car charger (surplus: %s W)", solar_surplus)

        # Set charge rate if entity is configured
        if should_charge and rate_entity and charge_rate > 0:
            await self._set_charge_rate(rate_entity, charge_rate)

        self._data["car_charger_active"] = should_charge
        self._data["car_charger_rate"] = charge_rate if should_charge else 0

    async def _set_charge_rate(self, rate_entity: str, rate: float) -> None:
        """Set the car charger rate."""
        try:
            # Try to set as a number entity
            await self.hass.services.async_call(
                "number", "set_value", 
                {"entity_id": rate_entity, "value": rate}
            )
            _LOGGER.debug("Set car charger rate to %s A", rate)
        except Exception as err:
            _LOGGER.warning("Could not set charge rate: %s", err)

    def get_data(self) -> dict[str, Any]:
        """Get current data."""
        return self._data

# Made with Bob
