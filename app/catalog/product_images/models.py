from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request

from app.database import Base
from urllib.parse import quote


class ProductImages(Base):
    __tablename__ = "product_images"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    description: Mapped[str] = mapped_column(nullable=True)
    logo: Mapped[bool] = mapped_column(Boolean, nullable=True)
    image_url: Mapped[str] = mapped_column(nullable=False)

    product = relationship("Products", back_populates="image")

    async def __admin_repr__(self, request: Request):
        return f"{self.image_url}"

    async def __admin_select2_repr__(self, request: Request) -> str:
        return f"<div><span>{self.description}</span></div>"

    
    @property
    def image_url_full(self) -> str:
        # нормализуем слэш и добавляем суффикс
        path = self.image_url.lstrip("/")
        if not path.endswith("_small.jpeg"):
            path = f"{path}_small.jpeg"
        # аккуратно кодируем кириллицу/пробелы, но оставляем служебные символы
       # return quote(path, safe="/:._-")
        return path
