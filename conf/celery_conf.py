from celery import Celery

from . import settings

app = Celery(
    main=settings.SYSTEM_CODENAME,
    # broker=settings.REDIS_BROKER_URL, # # TODO попробовать через RabbitMQ
)


class CeleryConfig:
    enable_utc: bool = True
    timezone: str = 'Europe/Moscow'
    task_always_eager: bool = settings.DEBUG


app.config_from_object(CeleryConfig)
app.autodiscover_tasks(
    packages=[
      "apps.document_types.tasks",
      "apps.section.tasks",
      "apps.signatory_authority.tasks",
    ]
)
