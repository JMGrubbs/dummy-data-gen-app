from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from core.config import settings
from schemas.user import UserLogin, UserCreate, AuthorizedUser, LoginResponse
from auth.dependencies import get_current_user
from services.auth import (
    InvalidCredentialsError,
    UpstreamAuthError,
    UserAlreadyExistsError,
    authenticate,
    logout,
    register,
)

router = APIRouter(tags=["auth"])

@router.post("/login")
async def login_route(
    credentials: UserLogin,
    response: Response,
) -> LoginResponse | dict[str, str | bool]:
    try:
        session = await authenticate(credentials)
        response.set_cookie(
            key=settings.cookie_key,
            value=session.token,
            httponly=True,
            secure=settings.cookie_secure,
            samesite="lax",
            max_age=60 * 60,
            expires=60 * 60,
            path="/",
        )
        return LoginResponse(username=session.user.username)
    except InvalidCredentialsError:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"ok": False, "message": "Invalid username or password"}
    except UpstreamAuthError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Authentication service unavailable")


@router.get("/me")
async def read_me_route(
    current_user: AuthorizedUser = Depends(get_current_user),
) -> dict[str, str]:
    return {"username": current_user.username}


@router.post("/logout")
async def logout_route(response: Response, request: Request) -> dict[str, bool]:
    token = request.cookies.get(settings.cookie_key)

    if token:
        await logout(token)
    response.delete_cookie(key=settings.cookie_key, path="/")
    return {"ok": bool(token)}


@router.post("/register")
async def register_route(
    new_user: UserCreate,
) -> dict[str, bool | str]:
    try:
        await register(new_user)
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except UpstreamAuthError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Unable to create user") from exc
    return {"ok": True, "message": "User created successfully"}

