"""Select platform for TCL+ AC."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SELECT_DESCRIPTIONS
from .coordinator import TclPlusCoordinator
from .entity import TclPlusPropertyEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up TCL+ select entities."""

    coordinator: TclPlusCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for device_id in coordinator.device_ids():
        props = coordinator.get_props(device_id)
        entities.extend(
            TclPlusSelect(coordinator, device_id, identifier, name, options)
            for identifier, (name, options) in SELECT_DESCRIPTIONS.items()
            if identifier in props
        )
    async_add_entities(entities)


class TclPlusSelect(TclPlusPropertyEntity, SelectEntity):
    """TCL+ enum property select."""

    def __init__(
        self,
        coordinator: TclPlusCoordinator,
        device_id: str,
        identifier: str,
        name: str,
        value_options: dict[int, str],
    ) -> None:
        super().__init__(coordinator, device_id, identifier, name)
        self._value_options = value_options
        self._label_to_value = {label: value for value, label in value_options.items()}

    @property
    def options(self) -> list[str]:
        return list(self._value_options.values())

    @property
    def current_option(self) -> str | None:
        try:
            value = int(self.current_value)
        except (TypeError, ValueError):
            return None
        return self._value_options.get(value)

    @property
    def available(self) -> bool:
        return super().available and not self.coordinator.is_disabled(self.device_id, self.identifier)

    async def async_select_option(self, option: str) -> None:
        """Select an option."""

        await self.coordinator.async_set_property(self.device_id, self.identifier, self._label_to_value[option])
