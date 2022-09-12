from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def a():
    from apps.section.logic.actions import refresh_npa_sections_subsections_from_source
    await refresh_npa_sections_subsections_from_source()
