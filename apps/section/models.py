from sqlalchemy import Boolean, Column, String, Text

from db.models import BaseModel


class NpaSection(BaseModel):
    """Блок НПА"""
    __tablename__ = "npa_sections"

    code: str = Column(String(length=64), unique=True, comment="Код")
    name: str = Column(String(length=512), unique=True, comment="Наименование")
    description: str = Column(Text(), comment="Описание", nullable=True)
    is_agencies_of_state_authorities: bool = Column(Boolean, comment="Орган государственной власти")

    def __str__(self) -> str:
        return self.name
