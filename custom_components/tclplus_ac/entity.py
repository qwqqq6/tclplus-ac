"""Shared entity helpers for TCL+ AC."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import TclPlusCoordinator


class TclPlusEntity(CoordinatorEntity[TclPlusCoordinator]):
    """Base entity for a TCL+ AC device."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: TclPlusCoordinator, device_id: str) -> None:
        super().__init__(coordinator)
        self.device_id = device_id

    @property
    def props(self) -> dict[str, Any]:
        return self.coordinator.get_props(self.device_id)

    @property
    def device(self) -> dict[str, Any]:
        return self.coordinator.get_device(self.device_id)

    @property
    def available(self) -> bool:
        online = self.device.get("isOnline")
        return super().available and online not in (0, "0", False)

    @property
    def device_info(self) -> DeviceInfo:
        device = self.device
        return DeviceInfo(
            identifiers={(DOMAIN, self.device_id)},
            name=device.get("nickName") or device.get("deviceName") or "TCL+ AC",
            manufacturer="TCL",
            model=device.get("model") or device.get("deviceType"),
            sw_version=device.get("firmwareVersion"),
            serial_number=self.device_id,
        )


class TclPlusPropertyEntity(TclPlusEntity):
    """Base entity tied to a single TCL property identifier."""

    def __init__(self, coordinator: TclPlusCoordinator, device_id: str, identifier: str, name: str) -> None:
        super().__init__(coordinator, device_id)
        self.identifier = identifier
        self._attr_name = name
        self._attr_unique_id = f"{device_id}_{identifier}"

    @property
    def current_value(self) -> Any:
        return self.props.get(self.identifier)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "disabled_by_app_rule": self.coordinator.is_disabled(self.device_id, self.identifier),
        }

    @property
    def available(self) -> bool:
        return super().available and self.identifier in self.props
