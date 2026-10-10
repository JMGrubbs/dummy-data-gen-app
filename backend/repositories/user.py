from schemas.user import UserLogin, LoginResponse
from services.auth import authenticate


async def login(user_login: UserLogin) -> dict[str, str | LoginResponse]:
    session = await authenticate(user_login)
    return {
        "token": session.token,
        "user": LoginResponse(username=session.user.username),
    }


