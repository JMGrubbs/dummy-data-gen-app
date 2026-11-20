from api.v1.endpoints import (
    auth,
    tasks,
    health,
    projects,
)
from fastapi import APIRouter

api_router = APIRouter()

# user endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# data endpoints
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(tasks.router, prefix="/projects", tags=["tasks"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])