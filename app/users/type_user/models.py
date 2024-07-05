from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TypeUser(Base):
    __tablename__ = "type_user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type_name: Mapped[str] = mapped_column(nullable=False, unique=True)