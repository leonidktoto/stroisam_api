from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request

from app.database import Base


class OrderItems(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), index=True, nullable=True
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=True)
    sum_price: Mapped[int] = mapped_column(nullable=True)

    product = relationship("Products", back_populates="orderitem")
    order = relationship("Orders", back_populates="orderitem")

    async def __admin_repr__(self, request: Request):
        return f"{self.product.product_name}, кол-во: {self.quantity}"

    async def __admin_select2_repr__(self, request: Request) -> str:
        return f"<div><span>{self.product.product_name}, кол-во: {self.quantity}</span></div>"
