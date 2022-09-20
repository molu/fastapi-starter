import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app.schemas.item import ItemCreate


@pytest.mark.anyio
async def test_create_item(client: AsyncClient):
    item_in = ItemCreate(name="Test item", value="Test item value", is_active=True)
    item_in_json = jsonable_encoder(item_in)
    response = await client.post("/items", json=item_in_json)
    assert response.status_code == 200
    assert response.json()["name"] == item_in.name
    assert response.json()["value"] == item_in.value
    assert response.json()["is_active"] == item_in.is_active
