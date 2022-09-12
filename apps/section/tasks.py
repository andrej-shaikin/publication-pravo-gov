import asyncio

from celery import shared_task

from apps.section.logic.actions import refresh_npa_sections_from_source, refresh_npa_sections_subsections_from_source


@shared_task
def refresh_npa_sections_from_source_task():
    """Периодическая задача для обновления блоков НПА из источника"""
    asyncio.run(refresh_npa_sections_from_source())


@shared_task
def refresh_npa_sections_subsections_from_source_task():
    """Периодическая задача для обновления блоков НПА из источника"""
    asyncio.run(refresh_npa_sections_subsections_from_source())
