from sqlalchemy import select

from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.orders.models import Orders
 

class OrdersDAO(BaseDAO):
    model = Orders

    @classmethod
    async def find_user_orders(
        cls,
        user_id,
        start_date=None,
        end_date=None,
        status=None,
    ):
        async with async_session_maker() as session:
            query = select(Orders).where(Orders.user_id == user_id)
            if start_date:
                query = query.where(Orders.order_date >= start_date)
            if end_date:
                query = query.where(Orders.order_date <= end_date)
            if status:
                query = query.where(Orders.order_status == status)
            result = await session.execute(query)
            return result.scalars().all()
