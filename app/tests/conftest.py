import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.main import app


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url=settings.BASE_URL + settings.API_PREFIX,
        headers={"Host": settings.DOMAIN},
    ) as client:
        yield client


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
