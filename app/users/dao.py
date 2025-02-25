from sqlalchemy import update

from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def update_by_phone(cls, phone: str, **kwargs):
        if not kwargs:
            raise ValueError("No data provided to update.")
        async with async_session_maker() as session:
            query = (
                update(cls.model).where(cls.model.id == id).values(**kwargs).returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()
