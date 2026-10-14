from fastapi import APIRouter
from fastapi import HTTPException, status

from services.health import dependencies_ready, live_payload
from schemas.data_generator import DataGeneratorResponse

router = APIRouter(tags=["data_generator"])

@router.get("gen", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def data_generator() -> dict[str, str]:
    return {"status": "ok"}
