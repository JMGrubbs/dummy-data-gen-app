import asyncio

from celery_app import celery_app
from repos import process_data_gen_task_async


@celery_app.task(
    name="data_gen.process_data_gen_task",
    bind=True,
    acks_late=True,
)
def process_data_gen_task(self, task_id: int) -> None:
    asyncio.run(process_data_gen_task_async(task_id))
