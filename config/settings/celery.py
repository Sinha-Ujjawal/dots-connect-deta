from datetime import timedelta
from .env_reader import env

# https://docs.celeryproject.org/en/stable/userguide/configuration.html

CELERY_BROKER_URL = env("DJANGO_CELERY_BROKER_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = "django-db"

CELERY_TIMEZONE = "UTC"

CELERY_TASK_SOFT_TIME_LIMIT = 20  # seconds
CELERT_TASK_TIME_LIMIT = 30  # seconds
CELERY_TASK_MAX_RETRIES = 3

CELERYBEAT_SCHEDULE = {
    "prune_stale_users_from_room": {
        "task": "dots_connect_deta.board.prune_stale_users_from_room",
        "schedule": timedelta(seconds=10),
    }
}
