import pytest
from httpx import AsyncClient

@pytest.mark.parametrize("date, status, count_orders, status_code", [
    ({"start_date": "2024-01-01", "end_date": "2024-02-02"}, {"status": "PROCESSING"}, 1, 200),
    ({"start_date": "2024-01-01", "end_date": "2024-03-03"}, {}, 3, 200),
    ({"start_date": "2024-03-03", "end_date": "2024-04-04"}, {}, 1, 200),
    ({"start_date": "2023-01-01", "end_date": "2023-03-03"}, {}, 0, 200),
    ({"start_date": "2023", "end_date": "2023-03-03"}, {}, 0, 422),
    ({"start_date": "2024-01-01", "end_date": "2024"}, {}, 0, 422),
    ({"start_date": "2024-01-01", "end_date": "2024-02-02"}, {"status": "CRTED"}, 0, 422),
    ({"start_date": "2024-01-01", "end_date": "2024-02-02"}, {"status": ""}, 0, 422),
])

@pytest.mark.asyncio
async def test_get_user_orders(date, status, count_orders, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/users/orders", params={**date, **status})
    assert response.status_code == status_code
    if status_code == 200:
        assert len(response.json()) == count_orders

