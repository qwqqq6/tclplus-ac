"""Climate platform for TCL+ AC."""

from __future__ import annotations

from typing import Any

from homeassistant.components.climate import ClimateEntity, ClimateEntityFeature, HVACMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    FAN_AUTO,
    FAN_MANUAL,
    HVAC_TO_WORK_MODE,
    PROP_CURRENT_TEMPERATURE,
    PROP_FAN_AUTO,
    PROP_HORIZONTAL_DIRECTION,
    PROP_HORIZONTAL_WIND,
    PROP_POWER,
    PROP_TARGET_TEMPERATURE,
    PROP_VERTICAL_DIRECTION,
    PROP_VERTICAL_WIND,
    PROP_WORK_MODE,
    SWING_BOTH,
    SWING_HORIZONTAL,
    SWING_HORIZONTAL_VALUE,
    SWING_OFF,
    SWING_OFF_VALUE,
    SWING_VERTICAL,
    SWING_VERTICAL_VALUE,
    TARGET_TEMPERATURE_MAX,
    TARGET_TEMPERATURE_MIN,
    TARGET_TEMPERATURE_STEP,
    WORK_MODE_TO_HVAC,
)
from .coordinator import TclPlusCoordinator
from .entity import TclPlusEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up TCL+ climate entities."""

    coordinator: TclPlusCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(TclPlusClimate(coordinator, device_id) for device_id in coordinator.device_ids())


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _hvac_mode_from_value(value: Any) -> HVACMode:
    hvac_value = WORK_MODE_TO_HVAC.get(_as_int(value), HVACMode.AUTO.value)
    return HVACMode(hvac_value)


class TclPlusClimate(TclPlusEntity, ClimateEntity):
    """TCL+ AC climate entity."""

    _attr_hvac_modes = [
        HVACMode.OFF,
        HVACMode.AUTO,
        HVACMode.COOL,
        HVACMode.DRY,
        HVACMode.FAN_ONLY,
        HVACMode.HEAT,
    ]
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.FAN_MODE
        | ClimateEntityFeature.SWING_MODE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_min_temp = TARGET_TEMPERATURE_MIN
    _attr_max_temp = TARGET_TEMPERATURE_MAX
    _attr_target_temperature_step = TARGET_TEMPERATURE_STEP
    _attr_fan_modes = [FAN_AUTO, FAN_MANUAL]
    _attr_swing_modes = [SWING_OFF, SWING_VERTICAL, SWING_HORIZONTAL, SWING_BOTH]

    def __init__(self, coordinator: TclPlusCoordinator, device_id: str) -> None:
        super().__init__(coordinator, device_id)
        self._attr_unique_id = f"{device_id}_climate"
        self._attr_name = None

    @property
    def hvac_mode(self) -> HVACMode:
        if _as_int(self.props.get(PROP_POWER)) == 0:
            return HVACMode.OFF
        return _hvac_mode_from_value(self.props.get(PROP_WORK_MODE))

    @property
    def target_temperature(self) -> float | None:
        return _as_float(self.props.get(PROP_TARGET_TEMPERATURE))

    @property
    def current_temperature(self) -> float | None:
        return _as_float(self.props.get(PROP_CURRENT_TEMPERATURE))

    @property
    def fan_mode(self) -> str:
        return FAN_AUTO if _as_int(self.props.get(PROP_FAN_AUTO)) == 1 else FAN_MANUAL

    @property
    def swing_mode(self) -> str:
        vertical_on = _as_int(self.props.get(PROP_VERTICAL_WIND)) == 1 or _as_int(self.props.get(PROP_VERTICAL_DIRECTION)) == SWING_VERTICAL_VALUE
        horizontal_on = _as_int(self.props.get(PROP_HORIZONTAL_WIND)) == 1 or _as_int(self.props.get(PROP_HORIZONTAL_DIRECTION)) == SWING_HORIZONTAL_VALUE
        if vertical_on and horizontal_on:
            return SWING_BOTH
        if vertical_on:
            return SWING_VERTICAL
        if horizontal_on:
            return SWING_HORIZONTAL
        return SWING_OFF

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        device = self.device
        return {
            "device_id": self.device_id,
            "product_key": device.get("productKey"),
            "work_mode": self.props.get(PROP_WORK_MODE),
            "vertical_direction": self.props.get(PROP_VERTICAL_DIRECTION),
            "horizontal_direction": self.props.get(PROP_HORIZONTAL_DIRECTION),
        }

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set HVAC mode."""

        if hvac_mode == HVACMode.OFF:
            await self.coordinator.async_set_property(self.device_id, PROP_POWER, 0)
            return

        work_mode = HVAC_TO_WORK_MODE[hvac_mode.value]
        if _as_int(self.props.get(PROP_POWER)) == 0:
            await self.coordinator.async_set_property(self.device_id, PROP_POWER, 1)
        await self.coordinator.async_set_property(self.device_id, PROP_WORK_MODE, work_mode)

    async def async_turn_on(self) -> None:
        """Turn the AC on."""

        await self.coordinator.async_set_property(self.device_id, PROP_POWER, 1)

    async def async_turn_off(self) -> None:
        """Turn the AC off."""

        await self.coordinator.async_set_property(self.device_id, PROP_POWER, 0)

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set target temperature."""

        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        await self.coordinator.async_set_property(self.device_id, PROP_TARGET_TEMPERATURE, temperature)

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set fan mode."""

        await self.coordinator.async_set_property(self.device_id, PROP_FAN_AUTO, 1 if fan_mode == FAN_AUTO else 0)

    async def async_set_swing_mode(self, swing_mode: str) -> None:
        """Set swing mode."""

        vertical = SWING_OFF_VALUE
        horizontal = SWING_OFF_VALUE
        if swing_mode in (SWING_VERTICAL, SWING_BOTH):
            vertical = SWING_VERTICAL_VALUE
        if swing_mode in (SWING_HORIZONTAL, SWING_BOTH):
            horizontal = SWING_HORIZONTAL_VALUE
        await self.coordinator.async_set_raw_params(
            self.device_id,
            [
                {PROP_VERTICAL_DIRECTION: vertical},
                {PROP_HORIZONTAL_DIRECTION: horizontal},
                {"selfLearn": 0},
            ],
        )
