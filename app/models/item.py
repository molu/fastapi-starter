from .base import BaseModel


class Item(BaseModel, table=True):
    name: str
    value: str
    is_active: bool
