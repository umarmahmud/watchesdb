import pytest
from httpx import AsyncClient

BASE_URL = "http://web-dev:80"

@pytest.mark.asyncio
async def test_get_manufacturers():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/manufacturers")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_manufacturer():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/manufacturers/Rolex")
        assert response.status_code == 200
        assert response.json()["manufacturer"] == "Rolex"
        assert response.json()["origin"] == "Swiss"


@pytest.mark.asyncio
async def test_create_manufacturer_unauthorized():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/manufacturers")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"