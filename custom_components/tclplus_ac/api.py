"""TCL+ domestic App API client."""

from __future__ import annotations

import base64
import hashlib
import json
import random
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from typing import Any

from .const import (
    ACCOUNT_BASE,
    APP_ID,
    APP_PACKAGE_NAME,
    APP_SECRET,
    APP_VERSION,
    APP_VERSION_NAME,
    DISABLE_RULES,
    IOT_BASE,
    LINK_RULES,
    SDK_VERSION,
    TENANT_ID,
)


class TclPlusError(Exception):
    """Base error for TCL+ failures."""


class TclPlusAuthError(TclPlusError):
    """Authentication failed."""


class TclPlusConnectionError(TclPlusError):
    """Connection failed."""


@dataclass
class AuthData:
    """Persisted account tokens."""

    username: str
    access_token: str
    refresh_token: str | None
    account_id: str | None
    client_device_id: str


def create_client_device_id() -> str:
    """Return a stable client id candidate for TCL account login."""

    return uuid.uuid4().hex


def _json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def _url(base: str, path: str, query: dict[str, Any] | None = None) -> str:
    url = base.rstrip("/") + "/" + path.lstrip("/")
    if query:
        url += "?" + urllib.parse.urlencode(query)
    return url


def _request(
    method: str,
    url: str,
    headers: dict[str, str] | None = None,
    body: Any | None = None,
) -> Any:
    data = None
    req_headers = dict(headers or {})
    if body is not None:
        data = _json_dumps(body).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json;charset=utf-8")

    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            text = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        if exc.code in (401, 403):
            raise TclPlusAuthError(f"HTTP {exc.code}: {text}") from exc
        raise TclPlusConnectionError(f"HTTP {exc.code}: {text}") from exc
    except OSError as exc:
        raise TclPlusConnectionError(str(exc)) from exc

    try:
        return json.loads(text) if text else {}
    except json.JSONDecodeError as exc:
        raise TclPlusConnectionError(f"Invalid JSON response from TCL+: {text[:200]}") from exc


def _account_query(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    query: dict[str, Any] = {"appId": APP_ID, "appSecret": APP_SECRET, "tenantId": TENANT_ID}
    if extra:
        query.update(extra)
    return query


def _report_state(client_device_id: str) -> str:
    return _json_dumps(
        {
            "versionName": APP_VERSION_NAME,
            "packageName": APP_PACKAGE_NAME,
            "platform": "android",
            "system": "Android",
            "systemCode": "15",
            "data": {"deviceId": client_device_id, "root": 0, "adb": 0, "emulator": 0},
        }
    )


def _walk_values(data: Any, key: str) -> Any:
    if isinstance(data, dict):
        if key in data and data[key] not in (None, ""):
            return data[key]
        for value in data.values():
            found = _walk_values(value, key)
            if found not in (None, ""):
                return found
    elif isinstance(data, list):
        for item in data:
            found = _walk_values(item, key)
            if found not in (None, ""):
                return found
    return None


def _jwt_payload(token: str | None) -> dict[str, Any]:
    if not token:
        return {}
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload.encode("utf-8")).decode("utf-8"))
    except (IndexError, ValueError, json.JSONDecodeError):
        return {}


def _jwt_exp(token: str | None) -> int | None:
    payload = _jwt_payload(token)
    exp = payload.get("exp")
    return int(exp) if isinstance(exp, (int, float)) else None


def _account_id_from_token(token: str | None) -> str | None:
    payload = _jwt_payload(token)
    user_info = payload.get("userInfo")
    if isinstance(user_info, str):
        try:
            user_info = json.loads(user_info)
        except json.JSONDecodeError:
            return None
    if isinstance(user_info, dict):
        account_id = user_info.get("accountId")
        return str(account_id) if account_id else None
    return None


def _extract_auth(username: str, client_device_id: str, response: Any) -> AuthData:
    access_token = _walk_values(response, "accessToken")
    refresh_token = _walk_values(response, "refreshToken")
    account_id = _walk_values(response, "accountId") or _account_id_from_token(access_token)
    error_code = _walk_values(response, "errorCode")
    message = _walk_values(response, "msg") or _walk_values(response, "message")

    if not access_token:
        if error_code or message:
            raise TclPlusAuthError(str(message or error_code))
        raise TclPlusAuthError("TCL+ login did not return an access token")

    return AuthData(
        username=username,
        access_token=str(access_token),
        refresh_token=str(refresh_token) if refresh_token else None,
        account_id=str(account_id) if account_id else None,
        client_device_id=client_device_id,
    )


def _coerce(value: Any) -> Any:
    if isinstance(value, str):
        text = value.strip()
        if text == "any":
            return text
        try:
            if "." in text:
                return float(text)
            return int(text)
        except ValueError:
            return text
    return value


def _compare(left: Any, operator: str, right: Any) -> bool:
    left = _coerce(left)
    right = _coerce(right)
    if right == "any":
        return True
    if operator == "==":
        return left == right
    if operator == "!=":
        return left != right
    try:
        left_num = float(left)
        right_num = float(right)
    except (TypeError, ValueError):
        return False
    if operator == ">":
        return left_num > right_num
    if operator == "<":
        return left_num < right_num
    if operator == ">=":
        return left_num >= right_num
    if operator == "<=":
        return left_num <= right_num
    return False


def _condition_matches(condition: tuple[str, str, Any], props: dict[str, Any]) -> bool:
    identifier, operator, value = condition
    if identifier not in props:
        return False
    return _compare(props.get(identifier), operator, value)


def _normalize_conditions(raw: Any) -> list[tuple[str, str, Any]]:
    if not raw:
        return []
    if isinstance(raw, tuple) and len(raw) == 3 and isinstance(raw[0], str):
        return [raw]
    return list(raw)


def disabled_identifiers(props: dict[str, Any]) -> set[str]:
    """Return identifiers disabled by the app panel rules."""

    disabled: set[str] = set()
    for raw_conditions, identifier in DISABLE_RULES:
        conditions = _normalize_conditions(raw_conditions)
        if all(_condition_matches(condition, props) for condition in conditions):
            disabled.add(identifier)
    return disabled


def linked_params(identifier: str, value: Any, props: dict[str, Any]) -> list[dict[str, Any]]:
    """Build the parameter list the app would send for a property change."""

    after = dict(props)
    after[identifier] = value
    params: list[dict[str, Any]] = [{identifier: value}]
    seen = {identifier}

    for rule in LINK_RULES:
        main_identifier, main_operator, main_value = rule["main"]
        if main_identifier != identifier or not _compare(value, main_operator, main_value):
            continue
        if not all(_condition_matches(condition, after) for condition in rule["when"]):
            continue
        for action in rule["actions"]:
            for action_id, action_value in action.items():
                after[action_id] = action_value
                if action_id in seen:
                    for param in params:
                        if action_id in param:
                            param[action_id] = action_value
                            break
                else:
                    params.append({action_id: action_value})
                    seen.add(action_id)

    return params


class TclPlusApi:
    """Synchronous TCL+ API wrapper."""

    def __init__(self, auth: AuthData) -> None:
        self.auth = auth
        self.tokens_changed = False

    @classmethod
    def login(cls, username: str, password: str, client_device_id: str | None = None) -> AuthData:
        """Login with username/password and return tokens."""

        device_id = client_device_id or create_client_device_id()
        body = {
            "username": username,
            "password": hashlib.md5(password.encode("utf-8")).hexdigest(),
            "channel": "app",
            "deviceId": device_id,
        }
        query = _account_query({"reportState": _report_state(device_id)})
        response = _request("POST", _url(ACCOUNT_BASE, "/auth/auth/login", query), body=body)
        return _extract_auth(username, device_id, response)

    def refresh_access_token(self) -> bool:
        """Refresh access token if possible."""

        if not self.auth.refresh_token or not self.auth.account_id:
            return False
        query = _account_query({"accountId": self.auth.account_id})
        response = _request(
            "GET",
            _url(ACCOUNT_BASE, "/auth/auth/refershToken", query),
            headers={"refreshToken": self.auth.refresh_token},
        )
        updated = _extract_auth(self.auth.username, self.auth.client_device_id, response)
        self.auth.access_token = updated.access_token
        self.auth.refresh_token = updated.refresh_token or self.auth.refresh_token
        self.auth.account_id = updated.account_id or self.auth.account_id
        self.tokens_changed = True
        return True

    def ensure_token(self) -> None:
        """Refresh token before it expires."""

        exp = _jwt_exp(self.auth.access_token)
        if exp is not None and exp - time.time() > 600:
            return
        self.refresh_access_token()

    def iot_headers(self, source_type: str | None = None) -> dict[str, str]:
        headers = {
            "platform": "android",
            "User-Agent": f"{APP_PACKAGE_NAME}/{SDK_VERSION}",
            "appPackageName": APP_PACKAGE_NAME,
            "systemVersion": "15",
            "brand": "HomeAssistant",
            "appVersion": APP_VERSION,
            "sdkVersion": SDK_VERSION,
            "accessToken": self.auth.access_token,
        }
        if source_type:
            headers["sourceType"] = source_type
        return headers

    def user_info(self) -> Any:
        self.ensure_token()
        return _request(
            "GET",
            _url(ACCOUNT_BASE, "/user/user/getUserInfoByToken", _account_query()),
            headers={"TCL-Authorization": self.auth.access_token},
        )

    def list_devices(self) -> dict[str, Any]:
        self.ensure_token()
        response = _request(
            "GET",
            _url(IOT_BASE, "/v1/tclplus/user/user_devices"),
            headers=self.iot_headers(),
        )
        if not isinstance(response, dict):
            raise TclPlusConnectionError("Unexpected TCL+ device list response")
        return response

    def set_property(self, device_id: str, params: list[dict[str, Any]]) -> dict[str, Any]:
        self.ensure_token()
        body = {
            "msgId": f"android_{random.randint(0, 96000)}_{int(time.time() * 1000)}",
            "version": "1.0",
            "params": params,
            "source": "APP",
        }
        response = _request(
            "POST",
            _url(IOT_BASE, f"/v1/control/property/{device_id}"),
            headers=self.iot_headers("2"),
            body=body,
        )
        if not isinstance(response, dict):
            raise TclPlusConnectionError("Unexpected TCL+ control response")
        return response

    def set_app_property(self, device_id: str, identifier: str, value: Any, props: dict[str, Any]) -> dict[str, Any]:
        """Set a property with the same linked params as the TCL+ panel."""

        return self.set_property(device_id, linked_params(identifier, value, props))

    def auth_data(self) -> dict[str, Any]:
        """Return serializable auth fields for Home Assistant config entries."""

        return {
            "username": self.auth.username,
            "access_token": self.auth.access_token,
            "refresh_token": self.auth.refresh_token,
            "account_id": self.auth.account_id,
            "client_device_id": self.auth.client_device_id,
        }
