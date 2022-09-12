import ormar

from fastapi_utils.db.models import BaseModel, BaseModelMeta


class DocumentType(BaseModel):
    """Тип документа"""
    name: str = ormar.String(max_length=512, index=True, unique=True)

    class Meta(BaseModelMeta):
        tablename = "document_types"

    def __repr__(self) -> str:
        return self.name
