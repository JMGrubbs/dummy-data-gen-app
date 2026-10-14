from typing import Any

from fastapi import APIRouter, status

router = APIRouter()


@router.post("/hook", status_code=status.HTTP_200_OK)
async def reciver(data: dict[Any, Any]) -> dict[str, str]:
    print("Received data:", data)
    return {"status": "ok"}
