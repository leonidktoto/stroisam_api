from pydantic import BaseModel, Field
from typing import List
from typing import Annotated
from datetime import datetime

from app.orders.models import OrderStatus

class SOrderItemsUpdate(BaseModel):
    product_id: int
    quantity: int
    price: int

class SOrderItemsUpdatePayload(BaseModel):
    items: List[SOrderItemsUpdate]



class SOrderFindPayload(BaseModel):
    order_id: Annotated[int, Field(gt=0, le=999_999_999)]

class SOrderStatusUpdate(BaseModel):
    order_status: OrderStatus

class SOrderDeliveryUpdate(BaseModel):
    desired_delivery_at: datetime | None = None