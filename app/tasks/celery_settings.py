from celery import Celery

from app.config import settings

app_celery = Celery("tasks", broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                    broker_connection_retry_on_startup=True, include=["app.tasks.tasks"])
