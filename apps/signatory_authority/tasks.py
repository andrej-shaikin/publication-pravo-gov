import asyncio

from celery import shared_task

from apps.signatory_authority.logic.actions import refresh_signatory_authority


@shared_task
def refresh_document_types_from_source_task():
    """Периодическая задача для обновления подписывающих органов из источника"""
    asyncio.run(refresh_signatory_authority())
