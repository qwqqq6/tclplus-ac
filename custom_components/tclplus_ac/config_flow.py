"""Config flow for TCL+ AC."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .api import TclPlusApi, TclPlusAuthError, TclPlusConnectionError, create_client_device_id
from .const import (
    CONF_ACCESS_TOKEN,
    CONF_ACCOUNT_ID,
    CONF_CLIENT_DEVICE_ID,
    CONF_REFRESH_TOKEN,
    DOMAIN,
)


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


async def _async_login(hass: HomeAssistant, username: str, password: str) -> dict[str, Any]:
    """Login in an executor and return config entry data."""

    client_device_id = create_client_device_id()
    auth = await hass.async_add_executor_job(TclPlusApi.login, username, password, client_device_id)
    return {
        CONF_USERNAME: auth.username,
        CONF_ACCESS_TOKEN: auth.access_token,
        CONF_REFRESH_TOKEN: auth.refresh_token,
        CONF_ACCOUNT_ID: auth.account_id,
        CONF_CLIENT_DEVICE_ID: auth.client_device_id,
    }


class TclPlusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for TCL+ AC."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""

        errors: dict[str, str] = {}

        if user_input is not None:
            username = user_input[CONF_USERNAME].strip()
            password = user_input[CONF_PASSWORD]

            try:
                data = await _async_login(self.hass, username, password)
            except TclPlusAuthError:
                errors["base"] = "invalid_auth"
            except TclPlusConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"
            else:
                unique_id = data.get(CONF_ACCOUNT_ID) or username
                await self.async_set_unique_id(str(unique_id))
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=f"TCL+ {username}", data=data)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
