import os

from celery import Celery
from kombu import Queue

celery_app = Celery(
    main="data_gen_worker",
    broker=os.environ["CELERY_BROKER_URL"],
)

celery_app.conf.update(
    task_default_queue="data-gen",
    task_queues=(Queue("data-gen"),),
    task_routes={
        "data_gen.*": {"queue": "data-gen"},
    },
    task_serializer="json",
    accept_content=["json"],
    task_ignore_result=True,  # might want to turn this on.
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
)
