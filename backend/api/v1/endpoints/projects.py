from typing import Any
from uuid import UUID
import json
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies import get_session
from auth.dependencies import get_current_user
from schemas.user import AuthorizedUser
from schemas.projects import (
    CreateProjectRequest,
    ProjectResponse,
    ProjectsResponse,
)

from services.projects import (
    get_projects,
    create_project,
    delete_project,
    update_project,
)

router = APIRouter()

def project_cache_key(
    user_id: UUID,
    project_id: UUID | None = None,
) -> str:
    return (
        f"projects:"
        f"{str(user_id).replace("-", "")}:"
        f"{str(project_id).replace("-", "") or 'all'}"
    )


@router.get("", summary="Get all projects for the current user")
@router.get("/{project_id}", summary="Get a specific project for the current user")
async def fetch_projects(
    request: Request,
    project_id: UUID | None = None,
    current_user: AuthorizedUser = Depends(get_current_user),
    db_client: AsyncSession = Depends(get_session),
) -> ProjectsResponse:
    redis: Redis = request.app.state.redis

    cache_key = project_cache_key(
        user_id=current_user.id,
        project_id=project_id
    )

    cached_projects = await redis.get(cache_key)

    if cached_projects is not None:
        return json.loads(cached_projects)

    user_projects: ProjectsResponse = await get_projects(
        db_client=db_client,
        user_id=current_user.id,
        project_id=project_id
    )

    encoded_projects = jsonable_encoder(user_projects)

    await redis.set(cache_key, json.dumps(encoded_projects), ex=20)

    return user_projects


@router.post("", summary="Create a new project for the current user")
async def new_project(
    request: Request,
    project_data: CreateProjectRequest,
    current_user: AuthorizedUser = Depends(get_current_user),
    db_client: AsyncSession = Depends(get_session),
) -> ProjectResponse:
    redis: Redis = request.app.state.redis

    new_project: ProjectResponse = await create_project(
        db_client=db_client,
        user_id=current_user.id,
        project_data=project_data
    )

    cache_key = project_cache_key(
        user_id=current_user.id,
        project_id=new_project.id
    )

    encoded_projects = jsonable_encoder(new_project)

    await redis.set(cache_key, json.dumps(encoded_projects), ex=20)

    return new_project


@router.delete("/{project_id}", summary="Delete a specific project for the current user")
async def remove_project(
    request: Request,
    project_id: UUID,
    current_user: AuthorizedUser = Depends(get_current_user),
    db_client: AsyncSession = Depends(get_session),
) -> dict[str, Any]:

    await delete_project(
        db_client=db_client,
        user_id=current_user.id,
        project_id=project_id
    )
    redis: Redis = request.app.state.redis

    cache_key = project_cache_key(
        user_id=current_user.id,
        project_id=project_id
    )

    if await redis.exists(cache_key):
        await redis.delete(cache_key)

    cache_key = project_cache_key(
        user_id=current_user.id,
        project_id=None
    )
    if await redis.exists(cache_key):
        await redis.delete(cache_key)


    return {"message": "Project deleted successfully"}


@router.put("/{project_id}", summary="Update a specific project for the current user")
async def edit_project(
    request: Request,
    project_id: UUID,
    project_data: CreateProjectRequest,
    current_user: AuthorizedUser = Depends(get_current_user),
    db_client: AsyncSession = Depends(get_session),
) -> ProjectResponse:
    redis: Redis = request.app.state.redis

    cache_key = project_cache_key(
        user_id=current_user.id,
        project_id=project_id
    )

    if await redis.exists(cache_key):
        await redis.delete(cache_key)

    updated_project: ProjectResponse = await update_project(
        db_client=db_client,
        user_id=current_user.id,
        project_id=project_id,
        project_data=project_data
    )

    cache_key = project_cache_key(
        user_id=current_user.id,
        project_id=updated_project.id
    )

    encoded_projects = jsonable_encoder(updated_project)

    await redis.set(cache_key, json.dumps(encoded_projects), ex=20)

    return updated_project
