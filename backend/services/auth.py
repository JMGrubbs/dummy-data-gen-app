"""Authentication service for the upstream identity API.

The application deliberately keeps identity data in the auth service.  This
module owns the HTTP contract with that service so route handlers can stay
small and return stable responses to the frontend.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from core.config import settings
from core.retry import build_http_retry
from httpx import HTTPError, HTTPStatusError, Response
from httpxC.http_client import http_client
from models.login_log import LoginLog
from schemas.auth import InvalidCredentialsError, UpstreamAuthError, UserAlreadyExistsError
from schemas.user import AuthorizedUser, UserCreate, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True, slots=True)
class AuthSession:
    token: str
    user: AuthorizedUser


def _endpoint(path: str) -> str:
    return f"{settings.auth_api_url.rstrip('/')}/api/v1/{path.lstrip('/')}"


def _json(response: Response) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError as exc:
        raise UpstreamAuthError("Auth service returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise UpstreamAuthError("Auth service returned an invalid response")
    return payload


def _token_from(payload: dict[str, Any]) -> str | None:
    for key in ("token", "access_token", "accessToken"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _user_from(payload: dict[str, Any]) -> AuthorizedUser:
    raw_id = payload.get("id")
    username = payload.get("username") or payload.get("email")
    if not isinstance(raw_id, str) or not isinstance(username, str):
        raise UpstreamAuthError("Auth service returned incomplete user data")
    try:
        user_id = __import__("uuid").UUID(raw_id)
    except (ValueError, AttributeError, TypeError) as exc:
        raise UpstreamAuthError("Auth service returned an invalid user id") from exc
    return AuthorizedUser(
        id=user_id,
        username=username,
        is_admin=bool(payload.get("is_admin", payload.get("isAdmin", False))),
    )


@build_http_retry(attempts=2)
async def _post_json(path: str, *, json: dict[str, Any], headers: dict[str, str] | None = None) -> Response:
    response = await http_client.post(_endpoint(path), json=json, headers=headers)
    response.raise_for_status()
    return response


@build_http_retry(attempts=2)
async def _get_json(path: str, *, headers: dict[str, str]) -> Response:
    response = await http_client.get(_endpoint(path), headers=headers)
    response.raise_for_status()
    return response


async def log_login(user: AuthorizedUser) -> None:
    """Log a successful login event upstream."""
    await _post_json(
        "auth/login/log",
        json={"user_id": str(user.id), "username": user.username},
    )


async def authenticate(
    credentials: UserLogin,
    db_session: AsyncSession,
) -> AuthSession:
    """Authenticate a user and resolve the resulting identity."""
    try:
        response: Response = await _post_json(
            "auth/login",
            # DAuth returns the token-bearing AuthorizedUserInternal shape only
            # for internal callers. The proxy needs that token to establish its
            # own cookie, while the public login shape intentionally omits it.
            json={"email": credentials.username, "password": credentials.password, "internal": True},
        )
    except HTTPStatusError as exc:
        if exc.response.status_code in {401, 403}:
            raise InvalidCredentialsError("Invalid username or password") from exc
        raise UpstreamAuthError("Auth service request failed") from exc
    except HTTPError as exc:
        raise UpstreamAuthError("Auth service request failed") from exc

    payload = _json(response)
    token = _token_from(payload)
    if token is None or payload.get("message"):
        raise InvalidCredentialsError("Invalid username or password")

    user_payload = payload.get("user") if isinstance(payload.get("user"), dict) else payload
    if not isinstance(user_payload, dict):
        raise UpstreamAuthError("Auth service returned no user data")
    user: AuthorizedUser = _user_from(user_payload)
    new_login_log = LoginLog(user_id=user.id, login_datetime=datetime.now())
    db_session.add(new_login_log)
    await db_session.commit()
    return AuthSession(token=token, user=user)


async def current_user(token: str) -> AuthorizedUser:
    """Resolve a bearer token through the upstream auth service."""
    if not token.strip():
        raise InvalidCredentialsError("Missing access token")
    try:
        response = await _get_json("auth/me", headers={"Authorization": f"Bearer {token}"})
    except HTTPStatusError as exc:
        if exc.response.status_code in {401, 403}:
            raise InvalidCredentialsError("Invalid or expired token") from exc
        raise UpstreamAuthError("Auth service request failed") from exc
    except HTTPError as exc:
        raise UpstreamAuthError("Auth service request failed") from exc
    payload = _json(response)
    return _user_from(payload)


async def register(credentials: UserCreate) -> str:
    """Create a user upstream and return its identifier."""
    try:
        response = await _post_json(
            "users/create",
            json={"email": credentials.username, "password": credentials.password},
        )
    except HTTPError as exc:
        raise UpstreamAuthError("Auth service request failed") from exc
    payload = _json(response)
    message = str(payload.get("message", ""))
    if "already exists" in message.lower() or "already registered" in message.lower():
        raise UserAlreadyExistsError(message)
    if payload.get("ok") is not True:
        raise UpstreamAuthError(message or "User creation failed")
    user_id = payload.get("user_id") or payload.get("id")
    return str(user_id) if user_id is not None else ""


async def logout(token: str) -> bool:
    """Invalidate an access token upstream."""
    if not token.strip():
        return False
    try:
        response = await _post_json("auth/logout", json={}, headers={"Authorization": f"Bearer {token}"})
    except (HTTPError, UpstreamAuthError):
        return False
    return response.is_success
