import asyncio

from celery import shared_task

from apps.document_types.logic.actions import refresh_document_types_from_source


@shared_task
def refresh_document_types_from_source_task():
    """Периодическая задача для обновления типов документов из источника"""
    asyncio.run(refresh_document_types_from_source())
