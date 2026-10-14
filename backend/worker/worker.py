import os

from celery import Celery

celery_client = Celery(
    main="data_gen_api",
    broker=os.environ["CELERY_BROKER_URL"],
)

# use this to send a task to the worker
# celery_client.send_task(
#     "data_gen.process_data_gen_task",
#     args=[new_task.id],
# )
