from api.v1.endpoints import (
    health,
    receiver,
)
from fastapi import APIRouter

api_router = APIRouter()

# data endpoints
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(receiver.router, prefix="/receiver", tags=["receiver"])
