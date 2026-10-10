from fastapi import Cookie, HTTPException, status, Request

from core.config import settings
from services.auth import AuthServiceError, current_user
from schemas.user import AuthorizedUser

def require_admin_user(request: Request) -> None:
    request_auth_key = request.headers.get("api-key")
    if not settings.admin_api_key or request_auth_key != settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

async def get_current_user(
    access_token: str | None = Cookie(default=None, alias=settings.cookie_key)
) -> AuthorizedUser:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        authorized_user = await current_user(access_token)
    except (AuthServiceError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return authorized_user
