from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from starlette.requests import Request



class Categories(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=True, index=True)
    category_name: Mapped[str] = mapped_column(nullable=False, index=True)
    image_url: Mapped[str] = mapped_column(nullable=True)
   
    parent = relationship("Categories", remote_side=[id])
    children = relationship("Categories", back_populates="parent")
    products=relationship("Products", back_populates="category")

    async def __admin_repr__(self, request: Request):
        return f"{self.category_name}"

    async def __admin_select2_repr__(self, request: Request) -> str:
            return f'<div><span>{self.category_name}</span></div>'