from sqlalchemy import Column, String

from db.models import BaseModel


class DocumentType(BaseModel):
    """Тип докуменaта"""
    __tablename__ = "document_types"

    name: str = Column(String(length=512), unique=True, comment="Наименование")

    def __str__(self) -> str:
        return self.name
