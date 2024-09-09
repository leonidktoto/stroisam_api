from re import L
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.DAO.base import BaseDAO
from app.carts.model import Carts
from app.catalog.products.models import Products
from app.database import async_session_maker

class CartsDAO(BaseDAO):
    model = Carts

    @classmethod
    async def get_user_cart(cls, id):
        async with async_session_maker() as session:
            query = select(
                Carts).options(joinedload(Carts.product)).where(Carts.user_id == id)
            result = await session.execute(query)
            result = result.scalars().all()

            if not result:
                return None 
            transform_result = []
            for item in result:
                product = {
                    "product_id" : item.id,
                    "article" : item.product.article,
                    "product_name" : item.product.product_name,
                    "quantity" : item.quantity,
                    "price" : item.price,
                    "sum_price" : item.sum_price,
                }
                transform_result.append(product)
            return transform_result

