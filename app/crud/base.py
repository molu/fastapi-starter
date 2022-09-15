from typing import Any, Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select
from sqlmodel.sql.expression import Select, SelectOfScalar

from app.models.base import BaseModel
from app.services.utils import get_logger, get_now

# SAWarning: Class SelectOfScalar will not make use of
# SQL compilation caching as it does not set the 'inherit_cache' attribute to ``True``.
Select.inherit_cache = True  # type: ignore
SelectOfScalar.inherit_cache = True  # type: ignore

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)

logger = get_logger()


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """CRUD object with default methods to Create, Read, Update, Delete (CRUD)."""
        self.model = model

    async def create(
        self, session: AsyncSession, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get(self, session: AsyncSession, id: UUID4) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == id)
        db_obj = await session.execute(stmt)
        item = db_obj.scalars().first()
        return item

    async def get_multi(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        db_obj = await session.execute(stmt)
        items = db_obj.scalars().all()
        return items

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str | Any],
    ) -> ModelType:
        db_obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in db_obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.updated_at = get_now()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, id: UUID4) -> None:
        db_obj = await self.get(session=session, id=id)
        if db_obj:
            await session.delete(db_obj)
            await session.commit()
        return None
