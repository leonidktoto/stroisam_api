from sqlalchemy import Boolean, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
from app.database import Base
from starlette.requests import Request
from datetime import datetime

created_at =Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
expires_at=Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())+ interval '10 minutes'"))]

class SmsCodes(Base):
    __tablename__="smscodes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    code: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    expires_at: Mapped[expires_at]
    is_used: Mapped[bool] = mapped_column(Boolean, server_default="False")

    user=relationship("Users", back_populates="sms")
    