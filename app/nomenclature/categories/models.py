from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Categories(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True, index=True)
    category_name: Mapped[str] = mapped_column(nullable=False)
   

   
   # def __str__(self):
   #     return self.name