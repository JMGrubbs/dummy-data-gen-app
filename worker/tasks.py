import asyncio
from typing import Any

from celery_app import celery_app
from repos import process_data_gen_task_async


@celery_app.task(
    name="data_gen.process_data_gen_task",
)
def process_data_gen_task(
    task_id: int,
    data: dict[str, Any],
) -> None:
    asyncio.run(process_data_gen_task_async(task_id, data))
