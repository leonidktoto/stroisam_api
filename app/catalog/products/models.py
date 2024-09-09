from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from starlette.requests import Request



class Products(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    article: Mapped[int] = mapped_column(index=True, nullable=True, unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    product_name: Mapped[str] = mapped_column(nullable=False, index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=True)
    stock: Mapped[int] = mapped_column(nullable=True)


    category = relationship("Categories", back_populates="products")
    product_attribute = relationship("ProductAttributes", back_populates="product", cascade="all, delete-orphan")
    image = relationship("ProductImages", back_populates="product", cascade="all, delete-orphan", order_by="ProductImages.logo.desc()")
    orderitem = relationship("OrderItems", back_populates='product')
    cart=relationship("Carts", back_populates="product", cascade="all, delete-orphan")

   

    async def __admin_repr__(self, request: Request): 
            return f"{self.product_name}"

    async def __admin_select2_repr__(self, request: Request) -> str:
            return f'<div><span>Артикул: {self.article}; Наименование: {self.product_name}</span></div>'

