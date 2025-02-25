from datetime import datetime

from pydantic import BaseModel, Field

from app.orders.models import OrderStatus


class SOrders(BaseModel):
    id: int
    user_id: int
    order_date: datetime
    total_amount: int | None
    order_status: OrderStatus


class SOrdersWithoutUserId(SOrders):
    user_id: int = Field(exclude=True)
