import pytest
from httpx import AsyncClient

BASE_URL = "http://web-dev:80"

@pytest.mark.asyncio
async def test_get_movements():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/movements")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_movement():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/movements/9S64")
        assert response.status_code == 200
        assert response.json()["movement"] == "9S64"
        assert response.json()["movement_type"] == "manual"
        assert response.json()["jewels"] == 24
        assert response.json()["power_reserve"] == 72
        assert response.json()["manufacturer"] == "Grand Seiko"


@pytest.mark.asyncio
async def test_create_movement_unauthorized():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/movements")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"