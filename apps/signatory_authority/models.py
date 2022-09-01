from sqlalchemy import Column, String

from db.models import BaseModel


class SignatoryAuthority(BaseModel):
    """Подписывающий орган"""
    __tablename__ = "signatory_authorities"

    name: str = Column(String(length=512), unique=True, comment="Наименование")

    def __str__(self) -> str:
        return self.name
