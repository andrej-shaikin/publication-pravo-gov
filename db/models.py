import uuid
from datetime import datetime

from fastapi_sqlalchemy import db
from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session

_Base = declarative_base()


class BaseModel(_Base):
    __abstract__ = True

    id: int = Column(
        type_=Integer(),
        primary_key=True,
        index=True,
        unique=True,
        autoincrement=True,
        nullable=False,
    )
    is_active: bool = Column(Boolean, default=True, comment="Активен")
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, comment="Уникальный идентификатор")
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата создания")
    updated_at: datetime = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="Дата последнего изменения",
    )

    objects = scoped_session(db.session)
