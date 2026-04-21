"""The Energy Flow Manager integration."""
from __future__ import annotations

import logging
import os
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.components import panel_custom
from homeassistant.util import file as file_util

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
    # Get the path to the panel HTML file
    panel_path = os.path.join(os.path.dirname(__file__), "panel.html")
    
    # Read the panel HTML content asynchronously
    panel_html = await hass.async_add_executor_job(
        file_util.read_file, panel_path
    )
    
    # Register the panel using panel_custom component
    await panel_custom.async_register_panel(
        hass,
        frontend_url_path=DOMAIN,
        webcomponent_name="energy-flow-panel",
        sidebar_title="Energy Flow",
        sidebar_icon="mdi:solar-power",
        module_url="/api/panel_custom/energy-flow-panel",
        embed_iframe=True,
        require_admin=False,
        config={"html": panel_html},
    )


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)

# Made with Bob
