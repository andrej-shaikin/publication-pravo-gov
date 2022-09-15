from datetime import date, datetime

import ormar
from fastapi_utils.db.models import BaseModel, BaseModelMeta

from apps.document_types.models import DocumentType
from apps.signatory_authority.models import SignatoryAuthority


class NpaSection(BaseModel):
    """Блок НПА"""
    __tablename__ = "npa_sections"

    code: str = ormar.String(max_length=64, unique=True, nullable=False)
    name: str = ormar.String(max_length=512, unique=True)
    description: str = ormar.Text(nullable=True)
    is_agencies_of_state_authorities: bool = ormar.Boolean()

    class Meta(BaseModelMeta):
        tablename = "npa_sections"

    def __repr__(self) -> str:
        return self.name


class NpaSubSection(BaseModel):
    """Подсекция секции НПА"""
    code: str = ormar.String(max_length=64, unique=True, nullable=False)
    name: str = ormar.String(max_length=512, unique=True)
    description: str = ormar.Text(nullable=True)
    is_agencies_of_state_authorities: bool = ormar.Boolean()
    npa_section: NpaSection = ormar.ForeignKey(
        to=NpaSection,
        related_name="sub_sections",
        index=True,
        ondelete="CASCADE",
    )

    class Meta(BaseModelMeta):
        tablename = "npa_subsections"

    def __repr__(self) -> str:
        return self.name


class NpaDocument(BaseModel):
    complex_name: str = ormar.String(max_length=5000)
    name: str = ormar.String(max_length=5000)
    document_date: date = ormar.Date(nullable=False)
    publish_date_short: datetime = ormar.DateTime(nullable=False)
    document_type: DocumentType = ormar.ForeignKey(DocumentType, nullable=True, skip_reverse=False)
    eo_number: str = ormar.String(max_length=16, unique=True)
    has_pdf: bool = ormar.Boolean()
    number: str = ormar.String(max_length=128, nullable=True)
    signatory_authority: SignatoryAuthority = ormar.ForeignKey(
        SignatoryAuthority,
        related_name="npa_documents",
        index=True,
        nullable=True,
    )

    class Meta(BaseModelMeta):
        tablename = "npa_documents"

    def __repr__(self) -> str:
        return f"№{self.eo_number}: {self.complex_name}"
