"""Config flow for Energy Flow Manager integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
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
    CONF_UPDATE_INTERVAL,
    DEFAULT_WATER_HEATER_MIN_SURPLUS,
    DEFAULT_WATER_HEATER_MIN_TEMP,
    DEFAULT_WATER_HEATER_MAX_TEMP,
    DEFAULT_WATER_HEATER_POWER,
    DEFAULT_CAR_CHARGER_MIN_SURPLUS,
    DEFAULT_CAR_CHARGER_MIN_RATE,
    DEFAULT_CAR_CHARGER_MAX_RATE,
    DEFAULT_BATTERY_MIN_SOC,
    DEFAULT_BATTERY_MAX_SOC,
    DEFAULT_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class EnergyFlowManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Energy Flow Manager."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Create the config entry
            return self.async_create_entry(
                title="Energy Flow Manager",
                data=user_input,
            )

        # Single-step schema with all configuration
        data_schema = vol.Schema(
            {
                # Input sensors
                vol.Required(CONF_SOLAR_SURPLUS_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Optional(CONF_BATTERY_SOC_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Optional(CONF_BATTERY_POWER_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Optional(CONF_WATER_TEMP_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                # Water heater
                vol.Optional(CONF_WATER_HEATER_SWITCH): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="switch")
                ),
                vol.Optional(
                    CONF_WATER_HEATER_MIN_SURPLUS,
                    default=DEFAULT_WATER_HEATER_MIN_SURPLUS,
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=10000)),
                vol.Optional(
                    CONF_WATER_HEATER_MIN_TEMP,
                    default=DEFAULT_WATER_HEATER_MIN_TEMP,
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
                vol.Optional(
                    CONF_WATER_HEATER_MAX_TEMP,
                    default=DEFAULT_WATER_HEATER_MAX_TEMP,
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
                vol.Optional(
                    CONF_WATER_HEATER_POWER,
                    default=DEFAULT_WATER_HEATER_POWER,
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=10000)),
                # Car charger
                vol.Optional(CONF_CAR_CHARGER_SWITCH): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="switch")
                ),
                vol.Optional(CONF_CAR_CHARGER_RATE_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="number")
                ),
                vol.Optional(
                    CONF_CAR_CHARGER_MIN_SURPLUS,
                    default=DEFAULT_CAR_CHARGER_MIN_SURPLUS,
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=10000)),
                vol.Optional(
                    CONF_CAR_CHARGER_MIN_RATE,
                    default=DEFAULT_CAR_CHARGER_MIN_RATE,
                ): vol.All(vol.Coerce(int), vol.Range(min=6, max=32)),
                vol.Optional(
                    CONF_CAR_CHARGER_MAX_RATE,
                    default=DEFAULT_CAR_CHARGER_MAX_RATE,
                ): vol.All(vol.Coerce(int), vol.Range(min=6, max=32)),
                # Battery and general
                vol.Optional(
                    CONF_BATTERY_MIN_SOC,
                    default=DEFAULT_BATTERY_MIN_SOC,
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
                vol.Optional(
                    CONF_BATTERY_MAX_SOC,
                    default=DEFAULT_BATTERY_MAX_SOC,
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
                vol.Optional(
                    CONF_UPDATE_INTERVAL,
                    default=DEFAULT_UPDATE_INTERVAL,
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> EnergyFlowManagerOptionsFlow:
        """Get the options flow for this handler."""
        return EnergyFlowManagerOptionsFlow(config_entry)


class EnergyFlowManagerOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Energy Flow Manager."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Manage the options."""
        if user_input is not None:
            # Update the config entry with new data
            self.hass.config_entries.async_update_entry(
                self.config_entry, data={**self.config_entry.data, **user_input}
            )
            return self.async_create_entry(title="", data={})

        # Get current values
        current_data = self.config_entry.data

        # Schema for all options including entity selections
        data_schema = vol.Schema(
            {
                # Input sensors
                vol.Optional(
                    CONF_SOLAR_SURPLUS_SENSOR,
                    default=current_data.get(CONF_SOLAR_SURPLUS_SENSOR),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Optional(
                    CONF_BATTERY_SOC_SENSOR,
                    default=current_data.get(CONF_BATTERY_SOC_SENSOR),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Optional(
                    CONF_BATTERY_POWER_SENSOR,
                    default=current_data.get(CONF_BATTERY_POWER_SENSOR),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Optional(
                    CONF_WATER_TEMP_SENSOR,
                    default=current_data.get(CONF_WATER_TEMP_SENSOR),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                # Water heater
                vol.Optional(
                    CONF_WATER_HEATER_SWITCH,
                    default=current_data.get(CONF_WATER_HEATER_SWITCH),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="switch")
                ),
                vol.Optional(
                    CONF_WATER_HEATER_MIN_SURPLUS,
                    default=current_data.get(CONF_WATER_HEATER_MIN_SURPLUS, DEFAULT_WATER_HEATER_MIN_SURPLUS),
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=10000)),
                vol.Optional(
                    CONF_WATER_HEATER_MIN_TEMP,
                    default=current_data.get(CONF_WATER_HEATER_MIN_TEMP, DEFAULT_WATER_HEATER_MIN_TEMP),
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
                vol.Optional(
                    CONF_WATER_HEATER_MAX_TEMP,
                    default=current_data.get(CONF_WATER_HEATER_MAX_TEMP, DEFAULT_WATER_HEATER_MAX_TEMP),
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
                vol.Optional(
                    CONF_WATER_HEATER_POWER,
                    default=current_data.get(CONF_WATER_HEATER_POWER, DEFAULT_WATER_HEATER_POWER),
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=10000)),
                # Car charger
                vol.Optional(
                    CONF_CAR_CHARGER_SWITCH,
                    default=current_data.get(CONF_CAR_CHARGER_SWITCH),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="switch")
                ),
                vol.Optional(
                    CONF_CAR_CHARGER_RATE_ENTITY,
                    default=current_data.get(CONF_CAR_CHARGER_RATE_ENTITY),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="number")
                ),
                vol.Optional(
                    CONF_CAR_CHARGER_MIN_SURPLUS,
                    default=current_data.get(CONF_CAR_CHARGER_MIN_SURPLUS, DEFAULT_CAR_CHARGER_MIN_SURPLUS),
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=10000)),
                vol.Optional(
                    CONF_CAR_CHARGER_MIN_RATE,
                    default=current_data.get(CONF_CAR_CHARGER_MIN_RATE, DEFAULT_CAR_CHARGER_MIN_RATE),
                ): vol.All(vol.Coerce(int), vol.Range(min=6, max=32)),
                vol.Optional(
                    CONF_CAR_CHARGER_MAX_RATE,
                    default=current_data.get(CONF_CAR_CHARGER_MAX_RATE, DEFAULT_CAR_CHARGER_MAX_RATE),
                ): vol.All(vol.Coerce(int), vol.Range(min=6, max=32)),
                # Battery and general
                vol.Optional(
                    CONF_BATTERY_MIN_SOC,
                    default=current_data.get(CONF_BATTERY_MIN_SOC, DEFAULT_BATTERY_MIN_SOC),
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
                vol.Optional(
                    CONF_BATTERY_MAX_SOC,
                    default=current_data.get(CONF_BATTERY_MAX_SOC, DEFAULT_BATTERY_MAX_SOC),
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
                vol.Optional(
                    CONF_UPDATE_INTERVAL,
                    default=current_data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema)

# Made with Bob
