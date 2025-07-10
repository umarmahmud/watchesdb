import pytest
from httpx import AsyncClient

BASE_URL = "http://web-dev:80"

@pytest.mark.asyncio
async def test_get_watches():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/watches")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_watch_integer():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/watches/1")
        assert response.status_code == 200
        assert response.json()["watch_id"] == 1
        assert response.json()["manufacturer"] is not None
        assert response.json()["model"] is not None


@pytest.mark.asyncio
async def test_get_watch_string():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/watches/Rolex")
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Input should be a valid integer, unable to parse string as an integer"


@pytest.mark.asyncio
async def test_filter_watches_no_params():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/watches/filter")
        assert response.status_code == 422
        assert response.json()["detail"] == "No query parameters provided."


@pytest.mark.asyncio
async def test_filter_watches_extra_param():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/watches/filter?dial")
        assert response.status_code == 422
        assert response.json()["detail"] == "Extra inputs are not permitted"


@pytest.mark.asyncio
async def test_filter_watches_case_diameter_integer():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/watches/filter?case_diameter=40")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_filter_watches_same_tag():
    async with AsyncClient(base_url=BASE_URL) as client:
        manufacturer_1 = "Rolex"
        manufacturer_2 = "Omega"
        response = await client.get(f"/watches/filter?manufacturer={manufacturer_1}&manufacturer={manufacturer_2}")
        assert response.status_code == 200
        response_manufacturers = [watch["manufacturer"] for watch in response.json()]
        assert manufacturer_1 in response_manufacturers
        assert manufacturer_2 in response_manufacturers


@pytest.mark.asyncio
async def test_create_watch_unauthorized():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/watches")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_favorites_unauthorized():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/watches/favorites")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_set_favorite_unauthorized():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/watches/favorites")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"