from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.DAO.base import BaseDAO
from app.orders.order_items.models import OrderItems
from app.database import async_session_maker


class OrdersItemsDAO(BaseDAO):
    model = OrderItems

    @classmethod
    async def detail_order(cls, order_id):
        async with async_session_maker() as session:
            query = (
                select(OrderItems)
                .options(joinedload(OrderItems.product))
                .where(OrderItems.order_id == order_id)
                .order_by(OrderItems.id.asc())
                )
            result = await session.execute(query)
            result = result.scalars().all()

            if not result:
                return None 
            transform_result = []
            for item in result:
                product = {
                    "id" : item.id,
                    "product_id" : item.product_id,
                    "article" : item.product.article,
                    "product_name" : item.product.product_name,
                    "quantity" : item.quantity,
                    "price" : item.price,
                    "sum_price" : item.sum_price,
                }
                transform_result.append(product)
            return transform_result