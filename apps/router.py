from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def a():
    from apps.document_types.logic.actions import refresh_document_types_from_source
    await refresh_document_types_from_source()
