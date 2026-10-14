from api.v1.endpoints import (
    health,
    reciver,
)
from fastapi import APIRouter

api_router = APIRouter()

# data endpoints
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(reciver.router, prefix="/reciver", tags=["reciver"])
