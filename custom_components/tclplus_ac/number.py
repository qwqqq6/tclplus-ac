"""Number platform for TCL+ AC."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, NUMBER_DESCRIPTIONS
from .coordinator import TclPlusCoordinator
from .entity import TclPlusPropertyEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up TCL+ number entities."""

    coordinator: TclPlusCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for device_id in coordinator.device_ids():
        props = coordinator.get_props(device_id)
        entities.extend(
            TclPlusNumber(coordinator, device_id, identifier, name, minimum, maximum, step, unit)
            for identifier, (name, minimum, maximum, step, unit) in NUMBER_DESCRIPTIONS.items()
            if identifier in props
        )
    async_add_entities(entities)


class TclPlusNumber(TclPlusPropertyEntity, NumberEntity):
    """TCL+ numeric property."""

    _attr_mode = NumberMode.SLIDER

    def __init__(
        self,
        coordinator: TclPlusCoordinator,
        device_id: str,
        identifier: str,
        name: str,
        minimum: float,
        maximum: float,
        step: float,
        unit: str,
    ) -> None:
        super().__init__(coordinator, device_id, identifier, name)
        self._attr_native_min_value = minimum
        self._attr_native_max_value = maximum
        self._attr_native_step = step
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self) -> float | None:
        try:
            return float(self.current_value)
        except (TypeError, ValueError):
            return None

    @property
    def available(self) -> bool:
        return super().available and not self.coordinator.is_disabled(self.device_id, self.identifier)

    async def async_set_native_value(self, value: float) -> None:
        """Set number value."""

        await self.coordinator.async_set_property(self.device_id, self.identifier, int(value))
