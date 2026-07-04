"""Sensor platform for TCL+ AC."""

from __future__ import annotations

import json
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SELF_CLEAN_STATUS_OPTIONS, SENSOR_DESCRIPTIONS
from .coordinator import TclPlusCoordinator
from .entity import TclPlusPropertyEntity

TEMPERATURE_IDENTIFIERS = {
    "currentTemperature",
    "internalUnitCoilTemperature",
    "externalUnitCoilTemperature",
    "externalUnitTemperature",
    "externalUnitExhaustTemperature",
}

UNIT_BY_IDENTIFIER = {
    "internalUnitFanSpeed": "rpm",
    "externalUnitFanSpeed": "rpm",
    "compressorFrequency": "Hz",
    "externalUnitElectricCurrent": "A",
    "externalUnitVoltage": "V",
    "windSpeedPercentage": "%",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up TCL+ sensor entities."""

    coordinator: TclPlusCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for device_id in coordinator.device_ids():
        props = coordinator.get_props(device_id)
        entities.extend(
            TclPlusSensor(coordinator, device_id, identifier, name)
            for identifier, name in SENSOR_DESCRIPTIONS.items()
            if identifier in props
        )
    async_add_entities(entities)


def _native_sensor_value(identifier: str, value: Any) -> Any:
    if identifier == "selfCleanStatus":
        try:
            return SELF_CLEAN_STATUS_OPTIONS.get(int(value), value)
        except (TypeError, ValueError):
            return value
    if identifier in ("verticalWind", "horizontalWind", "PTCStatus", "fourWayValveStatus"):
        if value in (1, "1", True):
            return "开启"
        if value in (0, "0", False):
            return "关闭"
    if identifier == "errorCode":
        if value in (None, "", [], "[]"):
            return "无"
        if isinstance(value, list):
            return ", ".join(str(item) for item in value) or "无"
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return value


class TclPlusSensor(TclPlusPropertyEntity, SensorEntity):
    """TCL+ read-only property sensor."""

    def __init__(self, coordinator: TclPlusCoordinator, device_id: str, identifier: str, name: str) -> None:
        super().__init__(coordinator, device_id, identifier, name)
        if identifier in TEMPERATURE_IDENTIFIERS:
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        elif identifier in UNIT_BY_IDENTIFIER:
            self._attr_native_unit_of_measurement = UNIT_BY_IDENTIFIER[identifier]

    @property
    def native_value(self) -> Any:
        return _native_sensor_value(self.identifier, self.current_value)
