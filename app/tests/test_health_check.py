import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"status": "OK!"}
