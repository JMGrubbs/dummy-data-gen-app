from api.v1.endpoints import (
    auth,
    data_generator,
    health,
)
from fastapi import APIRouter

api_router = APIRouter()

# user endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# data endpoints
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(data_generator.router, prefix="/gen", tags=["data generator"])
