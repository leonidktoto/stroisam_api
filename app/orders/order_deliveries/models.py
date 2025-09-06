from datetime import date
from enum import Enum
from typing import Annotated

from sqlalchemy import ForeignKey, Date, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TypeDecorator, DateTime

from app.database import Base


#class ISODateTime(TypeDecorator):
#    """TIMESTAMP WITH TIME ZONE, но умеет принимать ISO-строки при сравнении/INSERT/UPDATE."""
#    impl = DateTime(timezone=True)
#    cache_ok = True
#
#    def process_bind_param(self, value, dialect):
#        # Строку ISO → tz-aware datetime
#        if isinstance(value, str):
#            v = value
#            if v.endswith("Z"):
#                v = v[:-1] + "+00:00"
#            return datetime.fromisoformat(v)
#        return value
#
#    def coerce_compared_value(self, op, value):
#        # При col < value заставляем SA использовать наш тип (а не VARCHAR)
#        return self.impl

class OrderDeliveries(Base):
    __tablename__ = "order_deliveries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), index=True, nullable=False
    )

    desired_delivery_at: Mapped[date] = mapped_column(
        Date(),
        nullable=False,
        index=True,
    )

    country: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=False)
    recipient_name: Mapped[str] = mapped_column(nullable=True)
    phone_primary: Mapped[str] = mapped_column(nullable=True)
    phone_secondary: Mapped[str] = mapped_column(nullable=True)
    extra_info: Mapped[str] = mapped_column(nullable=True)
    
    order = relationship("Orders", back_populates="deliveries")


#    async def __admin_repr__(self, request: Request):
#        return f"{self.recipient_name or 'Получатель не указан'} — {self.address}"
#
#    async def __admin_select2_repr__(self, request: Request) -> str:
#        dt = self.desired_delivery_at.isoformat() if self.desired_delivery_at else "время не выбрано"
#        return f"<div><div><strong>{self.recipient_name or 'Без имени'}</strong></div><div>{self.address}</div><div>{dt}</div></div>"






