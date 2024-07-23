from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKeyConstraint
from app.database import Base
from enum import Enum
from sqlalchemy.sql import and_
from starlette.requests import Request



class ProductImages(Base):
    __tablename__ = "product_images"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    description: Mapped[str] = mapped_column( nullable=True)
    logo: Mapped[bool] = mapped_column(Boolean, nullable=True)
    image_url: Mapped[str] = mapped_column(nullable=False)

    product=relationship("Products", back_populates="image")

    async def __admin_repr__(self, request: Request): 
            return f"{self.image_url}"
    async def __admin_select2_repr__(self, request: Request) -> str:
            return f'<div><span>{self.description}</span></div>'

