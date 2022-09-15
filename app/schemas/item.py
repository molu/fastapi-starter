from sqlmodel import SQLModel


class ItemCreate(SQLModel):
    name: str
    value: str
    is_active: bool


class ItemRead(SQLModel):
    name: str
    value: str
    is_active: bool


class ItemUpdate(SQLModel):
    name: str
    value: str
    is_active: bool
