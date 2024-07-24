from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from starlette.requests import Request




class ProductAttributes(Base):
    __tablename__ = "product_attributes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    attribute_name_id: Mapped[str] = mapped_column(ForeignKey("attributes.id"), nullable=False)
    attribute_value: Mapped[str] = mapped_column(nullable=False)

    product = relationship("Products", back_populates="product_attribute")
 
    attribute_name = relationship("Attributes")

    async def __admin_repr__(self, request: Request):
        return f"{self.attribute_name.attribute_name}: {self.attribute_value}"


