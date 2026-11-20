from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from models.project import Project  # Assuming you have a Project model defined in your models module
from sqlalchemy.future import select
from schemas.projects import CreateProjectRequest, ProjectResponse, ProjectsResponse

async def get_projects(db_client: AsyncSession, user_id: UUID, project_id: UUID | None = None) -> ProjectsResponse:
    """
    Fetches projects for a given user from the database.

    Args:
        user_id (str): The ID of the user.
        project_id (str | None): The ID of a specific project to fetch. If None, fetches all projects for the user.

    Returns:
        dict[str, any]: A dictionary containing the user's projects.
    """

    # Placeholder implementation. Replace with actual database query logic.
    if project_id:
        # Fetch a specific project for the user
        result = await db_client.execute(
            select(Project).where(Project.user_id == user_id, Project.id == project_id)
        )
        project = result.scalar_one_or_none()
        if project:
            return ProjectsResponse(projects=[ProjectResponse(
                id=project.id,
                name=project.name,
                created_at=project.created_at.isoformat()
            )])
        else:
            return ProjectsResponse(projects=[])
    else:
        # Fetch all projects for the user
        result = await db_client.execute(
            select(Project).where(Project.user_id == user_id)
        )
        projects = result.scalars().all()
        return ProjectsResponse(projects=[
            ProjectResponse(
                id=project.id,
                name=project.name,
                created_at=project.created_at.isoformat()
            ) for project in projects
        ])


async def create_project(db_client: AsyncSession, user_id: UUID, project_data: CreateProjectRequest) -> ProjectResponse:
    """
    Creates a new project for a given user in the database.

    Args:
        user_id (str): The ID of the user.
        project_data (dict): A dictionary containing the project data.

    Returns:
        dict[str, any]: A dictionary containing the created project.
    """
    # Placeholder implementation. Replace with actual database insert logic.
    new_project: Project = Project(user_id=user_id, name=project_data.name)
    db_client.add(new_project)
    await db_client.commit()
    await db_client.refresh(new_project)

    project: ProjectResponse = ProjectResponse(
        id=new_project.id,
        name=new_project.name,
        created_at=new_project.created_at.isoformat()
    )
    return project


async def delete_project(db_client: AsyncSession, user_id: UUID, project_id: UUID) -> bool:
    """
    Deletes a project for a given user from the database.

    Args:
        user_id (str): The ID of the user.
        project_id (str): The ID of the project to delete.

    Returns:
        bool: True if the project was deleted, False otherwise.
    """
    # Placeholder implementation. Replace with actual database delete logic.
    result = await db_client.execute(
        select(Project).where(Project.user_id == user_id, Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    if project:
        await db_client.delete(project)
        await db_client.commit()
        return True
    return False


async def update_project(db_client: AsyncSession, user_id: UUID, project_id: UUID, project_data: CreateProjectRequest) -> ProjectResponse:
    """
    Updates a project for a given user in the database.

    Args:
        user_id (str): The ID of the user.
        project_id (str): The ID of the project to update.
        project_data (dict): A dictionary containing the updated project data.

    Returns:
        dict[str, any] | None: A dictionary containing the updated project, or None if the project was not found.
    """
    # Placeholder implementation. Replace with actual database update logic.
    result = await db_client.execute(
        select(Project).where(Project.user_id == user_id, Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if project:
        project.name = project_data.name
        await db_client.commit()
        await db_client.refresh(project)
        return ProjectResponse(
            id=project.id,
            name=project.name,
            created_at=project.created_at.isoformat()
        )
    else:
        raise ValueError("Project not found")