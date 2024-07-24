from datetime import datetime
from sqlalchemy import ForeignKey, func, event, text, select, update, event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import Annotated
from enum import Enum
from app.database import async_session_maker
from app.orders.order_items.models import OrderItems

order_date =Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class OrderStatus(Enum):
    CREATED = "CREATED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"



class Orders(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    order_date: Mapped[order_date]
    total_amount: Mapped[int] = mapped_column(nullable=True)
    order_status: Mapped[OrderStatus] = mapped_column(nullable=False , server_default="CREATED")

    user=relationship("Users", back_populates="orders")
    orderitem=relationship("OrderItems", back_populates="order")

