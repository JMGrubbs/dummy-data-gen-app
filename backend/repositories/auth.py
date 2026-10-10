from typing import Any

from schemas.user import AuthorizedUser, UserCreate, UserLogin
from services.auth import (
    AuthServiceError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    authenticate,
    current_user,
    logout,
    register,
)


async def login_user(username: str, password: str) -> str:
    session = await authenticate(UserLogin(username=username, password=password))
    return session.token


async def get_user_from_token(token: str) -> AuthorizedUser | None:
    try:
        return await current_user(token)
    except (AuthServiceError, ValueError, TypeError):
        return None


async def blacklist_token(token: str) -> bool:
    return await logout(token)


async def register_user(email: str, password: str) -> dict[str, Any]:
    try:
        user_id = await register(UserCreate(username=email, password=password))
        return {"ok": True, "user_id": user_id}
    except UserAlreadyExistsError as exc:
        return {"ok": False, "error": str(exc)}
    except (AuthServiceError, ValueError) as exc:
        return {"ok": False, "error": str(exc)}


async def internal_api_login() -> bool:
    """Deprecated compatibility shim for callers that used the old repository API."""
    return False
