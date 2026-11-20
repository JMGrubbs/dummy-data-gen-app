from pydantic import BaseModel

class CreateProjectRequest(BaseModel):
    name: str


class ProjectResponse(BaseModel):
    id: str
    name: str
    created_at: str


class ProjectsResponse(BaseModel):
    projects: list[ProjectResponse]