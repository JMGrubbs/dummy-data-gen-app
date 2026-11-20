from pydantic import BaseModel
from uuid import UUID

class CreateProjectRequest(BaseModel):
    name: str


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    created_at: str


class ProjectsResponse(BaseModel):
    projects: list[ProjectResponse]