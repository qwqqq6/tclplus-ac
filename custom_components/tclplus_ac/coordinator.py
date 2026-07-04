"""Data coordinator for TCL+ AC devices."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import TclPlusApi, TclPlusError, disabled_identifiers
from .const import DEFAULT_SCAN_INTERVAL_SECONDS, DOMAIN


class TclPlusCoordinator(DataUpdateCoordinator[dict[str, dict[str, Any]]]):
    """Coordinate polling and control for TCL+ AC devices."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, api: TclPlusApi) -> None:
        super().__init__(
            hass,
            logger=__import__("logging").getLogger(__name__),
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL_SECONDS),
        )
        self.config_entry = entry
        self.api = api

    async def _async_update_data(self) -> dict[str, dict[str, Any]]:
        try:
            response = await self.hass.async_add_executor_job(self.api.list_devices)
            data = self._parse_devices(response)
            if self.api.tokens_changed:
                new_data = dict(self.config_entry.data)
                new_data.update(self.api.auth_data())
                self.hass.config_entries.async_update_entry(self.config_entry, data=new_data)
                self.api.tokens_changed = False
            return data
        except TclPlusError as exc:
            raise UpdateFailed(str(exc)) from exc

    @staticmethod
    def _extract_device_list(response: dict[str, Any]) -> list[dict[str, Any]]:
        data = response.get("data")
        if isinstance(data, dict):
            devices = data.get("list") or data.get("deviceList") or []
            return devices if isinstance(devices, list) else []
        if isinstance(data, list):
            return data
        devices = response.get("list") or []
        return devices if isinstance(devices, list) else []

    @staticmethod
    def _props_from_device(device: dict[str, Any]) -> dict[str, Any]:
        props: dict[str, Any] = {}
        for item in device.get("identifiers") or []:
            if isinstance(item, dict) and item.get("identifier"):
                props[item["identifier"]] = item.get("value")
        return props

    def _parse_devices(self, response: dict[str, Any]) -> dict[str, dict[str, Any]]:
        devices: dict[str, dict[str, Any]] = {}
        for device in self._extract_device_list(response):
            if device.get("category") != "AC":
                continue
            device_id = str(device.get("deviceId"))
            props = self._props_from_device(device)
            devices[device_id] = {
                "device": device,
                "props": props,
                "disabled": disabled_identifiers(props),
            }
        return devices

    def device_ids(self) -> list[str]:
        """Return known AC device ids."""

        return sorted((self.data or {}).keys())

    def get_device(self, device_id: str) -> dict[str, Any]:
        """Return raw device metadata."""

        return (self.data or {}).get(device_id, {}).get("device", {})

    def get_props(self, device_id: str) -> dict[str, Any]:
        """Return current property map for a device."""

        return (self.data or {}).get(device_id, {}).get("props", {})

    def is_disabled(self, device_id: str, identifier: str) -> bool:
        """Return whether the app panel currently disables an identifier."""

        disabled = (self.data or {}).get(device_id, {}).get("disabled", set())
        return identifier in disabled

    async def async_set_property(self, device_id: str, identifier: str, value: Any) -> None:
        """Set a property and refresh state."""

        props = self.get_props(device_id)
        await self.hass.async_add_executor_job(self.api.set_app_property, device_id, identifier, value, props)
        await self.async_request_refresh()

    async def async_set_raw_params(self, device_id: str, params: list[dict[str, Any]]) -> None:
        """Set raw params and refresh state."""

        await self.hass.async_add_executor_job(self.api.set_property, device_id, params)
        await self.async_request_refresh()
