from fastapi import APIRouter
from fastapi import HTTPException, status

from services.health import dependencies_ready, live_payload

router = APIRouter(tags=["health"])


@router.get("")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def readiness_check() -> dict[str, str]:
    if not await dependencies_ready():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Dependencies are not ready")
    return {"status": "ready"}


@router.get("/live")
async def liveness_check() -> dict[str, str]:
    return live_payload()
