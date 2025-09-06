from datetime import datetime
from enum import Enum
from typing import Annotated

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from sqlalchemy.types import TypeDecorator, DateTime

class ISODateTime(TypeDecorator):
    impl = DateTime(timezone=True)
    cache_ok = True
    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            v = value[:-1] + "+00:00" if value.endswith("Z") else value
            return datetime.fromisoformat(v)
        return value
    def coerce_compared_value(self, op, value):
        return self.impl

#order_date = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class OrderStatus(Enum):
    CREATED = "CREATED"  # Создан
    PROCESSING = "PROCESSING"  # В обработке
    OPERATOR_PROCESSED = "OPERATOR_PROCESSED"  # Обработан оператором
    CONFIRMED = "CONFIRMED"  # Подтвержден
    AWAITING_PAYMENT = "AWAITING_PAYMENT"  # Ожидает оплату
    PAID = "PAID"  # Оплачен
    COMPLETED = "COMPLETED"  # Завершен
    CANCELED = "CANCELED"  # Отменен


class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    order_date: Mapped[datetime] = mapped_column(
        ISODateTime(), 
        server_default=text("TIMEZONE('utc', now())"),
        nullable=False,
        index=True,
    )

    total_amount: Mapped[int] = mapped_column(nullable=True)
    delivery_address: Mapped[str] = mapped_column(nullable=True)
    order_status: Mapped[OrderStatus] = mapped_column(nullable=False, server_default="CREATED")

    user = relationship("Users", back_populates="orders")
    orderitem = relationship("OrderItems", back_populates="order")
    deliveries = relationship("OrderDeliveries", back_populates="order")