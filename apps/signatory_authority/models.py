import ormar

from fastapi_utils.db.models import BaseModel, BaseModelMeta


class SignatoryAuthority(BaseModel):
    """Подписывающий орган"""
    name: str = ormar.String(max_length=512, unique=True)

    class Meta(BaseModelMeta):
        tablename = "signatory_authorities"

    def __repr__(self) -> str:
        return self.name
