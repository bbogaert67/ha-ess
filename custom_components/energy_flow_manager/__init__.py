"""The Energy Flow Manager integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.components import frontend
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
)
from .energy_manager import EnergyFlowManager

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Energy Flow Manager from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Get update interval from config
    update_interval = entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)

    # Create the energy manager
    energy_manager = EnergyFlowManager(hass, entry)

    # Create coordinator for updates
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=energy_manager.async_update,
        update_interval=timedelta(seconds=update_interval),
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator and manager
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "manager": energy_manager,
    }

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    await async_setup_services(hass, energy_manager)

    # Register update listener for config changes
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    # Register panel in sidebar
    await async_register_panel(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_setup_services(hass: HomeAssistant, manager: EnergyFlowManager) -> None:
    """Set up services for the integration."""
    
    async def handle_force_update(call):
        """Handle the force update service call."""
        await manager.async_update()
        _LOGGER.info("Force update triggered")

    hass.services.async_register(DOMAIN, "force_update", handle_force_update)


async def async_register_panel(hass: HomeAssistant) -> None:
    """Register the Energy Flow Manager panel."""
    if DOMAIN not in hass.data.get("frontend_panels", {}):
        # Register the panel using the frontend component
        await frontend.async_register_built_in_panel(
            hass,
            "iframe",
            "Energy Flow",
            "mdi:solar-power",
            DOMAIN,
            {"url": f"/local/community/{DOMAIN}/panel.html"},
            require_admin=False,
        )


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)

# Made with Bob
