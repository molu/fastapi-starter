import uuid
from datetime import datetime

from pydantic import UUID4
from sqlalchemy.ext.declarative import declared_attr
from sqlmodel import Field, SQLModel

from app.services.utils import get_now


class BaseModel(SQLModel):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=get_now())
    updated_at: datetime | None

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
