from typing import Type
from sqlalchemy import and_, delete, insert, select, update
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


    @classmethod
    async def update_data(cls, update_values: dict, **filters):
        if not update_values:
            raise ValueError("No data provided to update.")
        
        if not filters:
            raise ValueError("No filter conditions provided.")
        
        async with async_session_maker() as session:
            # Создаем условия для фильтрации из **kwargs
            filter_conditions = [getattr(cls.model, key) == value for key, value in filters.items()]
            
            # Формирование запроса с фильтрацией и обновлением
            query = update(cls.model).where(and_(*filter_conditions)).values(**update_values).returning(cls.model)
            result = await session.execute(query)
            await session.commit()

            updated_row = result.scalar_one_or_none()

            if updated_row is None:
                raise ValueError(f"No row found with filters: {filters}")

            return updated_row