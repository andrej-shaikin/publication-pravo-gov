from celery import Celery
from dateutil.relativedelta import relativedelta

from . import settings

app = Celery(
    main=settings.SYSTEM_CODENAME,
    # broker=settings.REDIS_BROKER_URL, # # TODO попробовать через RabbitMQ
)

SIGNATORY_AUTHORITY_BEAT_SCHEDULES = {
    "refresh_document_types_from_source_task": {
        "task": "apps.signatory_authority.tasks.refresh_document_types_from_source_task",
        "schedule": relativedelta(days=1)
    }
}

DOCUMENT_TYPE_BEAT_SCHEDULE = {
    "refresh_document_types_from_source_task": {
        "task": "apps.document_types.tasks.refresh_document_types_from_source_task",
        "schedule": relativedelta(days=1)
    }
}

SECTION_BEAT_SCHEDULE = {
    "refresh_npa_sections_from_source_task": {
        "task": "apps.section.tasks.refresh_npa_sections_from_source_task",
        "schedule": relativedelta(days=1)
    },
    "refresh_npa_sections_subsections_from_source_task": {
        "task": "apps.section.tasks.refresh_npa_sections_subsections_from_source_task",
        "schedule": relativedelta(days=1)
    }
}


class CeleryConfig:
    enable_utc = True
    timezone = 'Europe/Moscow'
    task_always_eager = settings.DEBUG
    task_serializer = "json"
    result_serializer = "json"
    beat_schedules = {
        **SIGNATORY_AUTHORITY_BEAT_SCHEDULES,
        **DOCUMENT_TYPE_BEAT_SCHEDULE,
        **SECTION_BEAT_SCHEDULE,
    }


app.config_from_object(CeleryConfig)
app.autodiscover_tasks(
    packages=[
        "apps.document_types.tasks",
        "apps.section.tasks",
        "apps.signatory_authority.tasks",
    ]
)
