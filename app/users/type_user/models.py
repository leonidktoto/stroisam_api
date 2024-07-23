from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request
from app.database import Base


class TypeUser(Base):
    __tablename__ = "type_user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type_name: Mapped[str] = mapped_column(nullable=False, unique=True)

    user=relationship("Users", back_populates='type_')

    async def __admin_repr__(self, request: Request):
        return f"{self.type_name}"

    async def __admin_select2_repr__(self, request: Request) -> str:
            return f'<div><span>{self.type_name}</span></div>'