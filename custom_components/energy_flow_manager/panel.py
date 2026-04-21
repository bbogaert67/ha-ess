"""Panel for Energy Flow Manager."""
from __future__ import annotations

from homeassistant.components import frontend
from homeassistant.core import HomeAssistant


async def async_register_panel(hass: HomeAssistant) -> None:
    """Register the Energy Flow Manager panel."""
    await frontend.async_register_built_in_panel(
        hass,
        component_name="iframe",
        sidebar_title="Energy Flow",
        sidebar_icon="mdi:solar-power",
        frontend_url_path="energy-flow-manager",
        config={
            "url": "/api/hassio_ingress/energy_flow_manager",
        },
        require_admin=False,
    )

# Made with Bob
