from typing import Type
from sqlalchemy import delete, insert, select
from app.database import async_session_maker


class BaseDAO:
    model: Type  # Это позволяет явно указать, что model должен быть классом (типом) объекта.

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add_data(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().all()[0]

    @classmethod
    async def delete_by_id(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model.__table__).filter_by(**filter_by)
            result = await session.execute(query)
            await session.commit()