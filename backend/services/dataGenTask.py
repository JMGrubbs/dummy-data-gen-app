import uuid

from models.data_gen_task import DataGenTask
from schemas.dataGetTask import PackageFormat
from sqlalchemy.ext.asyncio import AsyncSession
from worker.worker import celery_client


async def load_data_gen_task(task: PackageFormat, db_session: AsyncSession) -> None:
    """
    Load a data generation task into the system.

    Args:
        task (DataGenTask): The data generation task to be loaded.

    Returns:
        None
    """

    new_task = DataGenTask(
        user_id=uuid.UUID("c0e29633-7077-400a-ad92-5f5387a45df4"),
        url_destination=str(task.url_destination),
        data_bp=task.data,
        remaining_requests=task.number_of_requests,
        requests_per_min=task.requests_per_min,
    )

    db_session.add(new_task)
    await db_session.flush()
    await db_session.commit()

    celery_client.send_task(
        name="data_gen.process_data_gen_task",
        args=[
            new_task.id,
            {
                "user_id": str(new_task.user_id),
                "url_destination": new_task.url_destination + "/api/v1/receiver/hook",
                "data_bp": new_task.data_bp,
                "remaining_requests": new_task.remaining_requests,
                "requests_per_min": new_task.requests_per_min,
            },
        ],
        queue="data-gen",
    )
