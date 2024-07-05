from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Products(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    article: Mapped[int] = mapped_column(index=True, nullable=False, unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    product_name: Mapped[str] = mapped_column(nullable=False, index=True)
    description: Mapped[str]  
    price: Mapped[int]
    stock: Mapped[int]
   