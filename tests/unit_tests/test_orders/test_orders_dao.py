from datetime import datetime

import pytest

from app.orders.dao import OrdersDAO
from app.orders.order_items.dao import OrdersItemsDAO


@pytest.mark.parametrize(
    "user_id, start_date, end_date, status , count",
    [
        (5, None, None, None, 3),
        (5, None, None, "COMPLETED", 1),
        (5, None, None, "PROCESSING", 1),
        (5, datetime(2024, 1, 3), None, None, 2),
        (5, datetime(2024, 1, 3), datetime(2024, 2, 3), None, 1),
        (5, datetime(2024, 1, 1), datetime(2024, 2, 1), None, 1),
        (5, datetime(2024, 1, 1), datetime(2024, 2, 2), None, 2),
        (5, datetime(2024, 1, 1), datetime(2024, 2, 2), "COMPLETED", 1),
        (1, None, None, None, None),
    ],
)
@pytest.mark.asyncio
async def test_find_user_orders(user_id, start_date, end_date, status, count):
    orders = await OrdersDAO.find_user_orders(
        user_id=user_id, start_date=start_date, end_date=end_date, status=status
    )
    if orders:
        assert len(orders) == count
        assert orders[0].user_id == user_id


@pytest.mark.parametrize("order_id, count", [(4, 2), (5, 3), (55, 0)])
@pytest.mark.asyncio
async def test_detail_order(order_id, count):
    order = await OrdersItemsDAO.detail_order(order_id)

    if order:
        assert len(order) == count
        assert order[0]["product_id"] == 1
        assert order[0]["quantity"] == 1
        assert order[0]["price"] == 100
