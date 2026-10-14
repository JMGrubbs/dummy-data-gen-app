from fastapi import APIRouter, status

router = APIRouter(tags=["reciver endpoints"])


@router.post("/test", status_code=status.HTTP_200_OK)
async def recive() -> dict[str, str]:
    return {"status": "ok"}
