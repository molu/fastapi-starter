import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.anyio
async def test_healthcheck(client: AsyncClient):
    response = await client.get(f"{settings.API_STR}/health-check")
    assert response.status_code == 200
    assert response.json() == {"status": "OK!"}
