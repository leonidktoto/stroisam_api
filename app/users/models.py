from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from starlette.requests import Request

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    type_user_id: Mapped[int] = mapped_column(ForeignKey("type_user.id"), nullable=False, server_default="1")
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="True")
    is_confirmed: Mapped[bool] = mapped_column(Boolean, server_default="False")
    registration_attempts: Mapped[int] = mapped_column(nullable=True, server_default="0")
    discount: Mapped[int] = mapped_column(nullable=True,server_default="0")


    type_=relationship("TypeUser", back_populates="user")
    sms=relationship("SmsCodes", back_populates="user")
    orders=relationship("Orders", back_populates="user")
    cart=relationship("Carts", back_populates="user")
    
    async def __admin_repr__(self, request: Request):
        return f"{self.type_.type_name}: {self.first_name} {self.last_name}, тел. {self.phone}"

    async def __admin_select2_repr__(self, request: Request) -> str:
            return f'<div><span>{self.type_.type_name}: {self.first_name} {self.last_name}, тел. {self.phone}</span></div>'