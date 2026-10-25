import os

from celery import Celery

celery_app = Celery(
    "data_gen_worker",
    broker=os.environ["CELERY_BROKER_URL"],
    include=["tasks"],
)

celery_app.conf.update(
    task_default_queue="data-gen",
    task_default_queue_type="quorum",
    broker_transport_options={"confirm_publish": True},
    task_ignore_result=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
    control_queue_exclusive=True,
    event_queue_exclusive=True,
)
