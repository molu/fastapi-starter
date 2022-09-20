from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db.session import get_session
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.services.exceptions import NotFoundException

router = APIRouter()


@router.post("/items", status_code=status.HTTP_200_OK)
async def create_item(
    item_in: ItemCreate, session: AsyncSession = Depends(get_session)
) -> ItemRead:
    item = await crud.item.create(session=session, obj_in=item_in)
    return item


@router.get("/items", status_code=status.HTTP_200_OK)
async def get_items(session: AsyncSession = Depends(get_session)) -> list[ItemRead]:
    items = await crud.item.get_multi(session=session)
    return items


@router.get("/items/{item_id}", status_code=status.HTTP_200_OK)
async def get_item(
    item_id: UUID4, session: AsyncSession = Depends(get_session)
) -> ItemRead:
    items = await crud.item.get(session=session, id=item_id)
    return items


@router.put("/items/{item_id}", status_code=status.HTTP_200_OK)
async def update_item(
    item_id: UUID4, item_in: ItemUpdate, session: AsyncSession = Depends(get_session)
) -> ItemRead:
    item_obj = await crud.item.get(session=session, id=item_id)
    if item_obj:
        item = await crud.item.update(session=session, db_obj=item_obj, obj_in=item_in)
    else:
        raise NotFoundException(msg=f"Item {item_id} not found")
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: UUID4, session: AsyncSession = Depends(get_session)
) -> None:
    await crud.item.delete(session=session, id=item_id)
    return None
