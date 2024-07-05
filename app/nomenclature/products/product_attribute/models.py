from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ProductAttribute(Base):
    __tablename__ = "product_attributes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    attribute_name: Mapped[str] 
    attribute_value: Mapped[str]
 

