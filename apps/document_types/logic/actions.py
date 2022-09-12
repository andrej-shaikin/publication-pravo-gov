from fastapi import APIRouter

from apps.document_types.logic.getters import get_document_types_from_source
from apps.document_types.models import DocumentType

router = APIRouter()


async def refresh_document_types_from_source() -> None:
    for document_type in await get_document_types_from_source():
        await DocumentType.objects.update_or_create(uuid=document_type.uuid, defaults={"name": document_type.name})
