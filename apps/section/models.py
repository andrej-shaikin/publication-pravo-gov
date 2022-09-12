import ormar

from fastapi_utils.db.models import BaseModel, BaseModelMeta


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
