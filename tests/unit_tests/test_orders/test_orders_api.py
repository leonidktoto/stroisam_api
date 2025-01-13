from os import stat
import pytest
from httpx import AsyncClient

from app.orders.order_items.dao import OrdersItemsDAO

test_data = [
    (1, 200), # заказ в котором есть товары
    (0, 400),
    (-1, 400),
]

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


@pytest.mark.parametrize("product, status_code", [
        
        (
            {
                "product_id": 1,
                "quantity": 1    
            }, 
            200
        ),
        (   
            {}, 
            400
        )
    ]
)
@pytest.mark.asyncio
async def test_create_order(product, status_code, authenticated_ac: AsyncClient):
    if product:
        response = await authenticated_ac.post("/users/cart/items", json=product, follow_redirects=True)
        assert response.status_code == status_code
    response = await authenticated_ac.post("/users/orders/checkout")
    assert response.status_code == status_code


@pytest.mark.parametrize("order_id, status_code", test_data)
@pytest.mark.asyncio
async def test_get_order_detail(order_id, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.get(f"/users/orders/{order_id}")
    assert response.json() is not None
    assert response.status_code == status_code
    if status_code == 200:
        assert len(response.json()) > 0
        assert "id" in response.json()[0]
        assert "product_id" in response.json()[0]
        assert "article" in response.json()[0]
        assert "product_name" in response.json()[0]
        assert "quantity" in response.json()[0]
        assert "price" in response.json()[0]
        assert "sum_price" in response.json()[0]

@pytest.mark.parametrize("order_id, status_code", test_data)
@pytest.mark.asyncio
async def test_cancel_order(order_id, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post(f"/users/orders/{order_id}/cancel")
    assert response.status_code == status_code


@pytest.mark.parametrize("order_id, status_code", test_data)
@pytest.mark.asyncio
async def test_reorder_order(order_id, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post(f"/users/orders/{order_id}/reorder")
    assert response.status_code == status_code