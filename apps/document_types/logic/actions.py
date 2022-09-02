from apps.document_types.logic.getters import get_document_types_from_source
from fastapi_sqlalchemy import db
from apps.document_types.models import DocumentType


from fastapi import APIRouter

router = APIRouter()



async def refresh_document_types_from_source() -> None:
    document_types = await get_document_types_from_source()
    b = DocumentType
    a = await get_document_types_from_source()
    a = db.session.query(DocumentType).all()
    b = 1
