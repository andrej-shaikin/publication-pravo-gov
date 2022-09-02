from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy_get_or_create import update_or_create

from apps.document_types.logic.getters import get_document_types_from_source
from apps.document_types.models import DocumentType

router = APIRouter()


async def refresh_document_types_from_source() -> None:
    for document_type in await get_document_types_from_source():
        update_or_create(
            session=db.session,
            model=DocumentType,
            uuid=document_type.uuid,
            defaults={"name": document_type.name},
        )
        db.session.commit()
