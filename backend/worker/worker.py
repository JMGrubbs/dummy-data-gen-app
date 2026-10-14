import os

from celery import Celery

celery_client = Celery(
    main="data_gen_api",
    broker=os.environ["CELERY_BROKER_URL"],
)

celery_client.conf.update(
    task_create_missing_queue_type="quorum",
    broker_transport_options={"confirm_publish": True},
)
