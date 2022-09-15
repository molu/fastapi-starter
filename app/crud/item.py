from app.models import Item
from app.schemas import ItemCreate, ItemUpdate

from .base import CRUDBase


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    pass


item: CRUDItem = CRUDItem(Item)
