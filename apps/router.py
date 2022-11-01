from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def a():
    from apps.section.logic.actions import refresh_npa_documents_from_source
    # from apps.section.tasks import refresh_npa_sections_subsections_from_source_task
    # TODO убрать аргументы чтобы были дефолтные
    # max - 5034
    await refresh_npa_documents_from_source(start_page=91, end_page=100)
    # await refresh_npa_sections_subsections_from_source_task()
