from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column
from starlette.requests import Request

from app.database import Base


class Attributes(Base):
    __tablename__ = "attributes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    attribute_name: Mapped[str] = mapped_column(nullable=False)
    filtered: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="False")

    # attributes = relationship("ProductAttribute", back_populates="attribute_name")

    async def __admin_repr__(self, request: Request):
        return f"{self.attribute_name}"

    async def __admin_select2_repr__(self, request: Request) -> str:
        return f"<div><span>{self.attribute_name}</span></div>"
