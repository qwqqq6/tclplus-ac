"""Switch platform for TCL+ AC."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SWITCH_DESCRIPTIONS
from .coordinator import TclPlusCoordinator
from .entity import TclPlusPropertyEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up TCL+ switch entities."""

    coordinator: TclPlusCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for device_id in coordinator.device_ids():
        props = coordinator.get_props(device_id)
        entities.extend(
            TclPlusSwitch(coordinator, device_id, identifier, name)
            for identifier, name in SWITCH_DESCRIPTIONS.items()
            if identifier in props
        )
    async_add_entities(entities)


class TclPlusSwitch(TclPlusPropertyEntity, SwitchEntity):
    """TCL+ bool property switch."""

    @property
    def is_on(self) -> bool:
        return self.current_value in (1, "1", True)

    @property
    def available(self) -> bool:
        return super().available and not self.coordinator.is_disabled(self.device_id, self.identifier)

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""

        await self.coordinator.async_set_property(self.device_id, self.identifier, 1)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""

        await self.coordinator.async_set_property(self.device_id, self.identifier, 0)
