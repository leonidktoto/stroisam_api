from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_get_main_categories(ac: AsyncClient):
    response = await ac.get("/categories/main", follow_redirects=True)
    assert response.status_code == 200


