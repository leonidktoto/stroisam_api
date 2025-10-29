from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.carts.models import Carts
from app.DAO.base import BaseDAO
from app.catalog.products.models import Products
from app.database import async_session_maker


class CartsDAO(BaseDAO):
    model = Carts

    @classmethod
    async def get_user_cart(cls, user_id):
        async with async_session_maker() as session:
            query = (
                select(Carts)
                .options(
                    selectinload(Carts.product).selectinload(Products.image)
                )
                .where(Carts.user_id == user_id)
                .order_by(Carts.id.asc())
            )
            result = await session.execute(query)
            result = result.scalars().all()

            if not result:
                return None

            transform_result = []
            for item in result:
                logo_image = None
                if item.product.image:
                    for img in item.product.image:
                        if getattr(img, "logo", False):
                            logo_image = getattr(img, "image_url", None)
                            break

                product = {
                    "id": item.id,
                    "product_id": item.product_id,
                    "article": item.product.article,
                    "product_name": item.product.product_name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "sum_price": item.sum_price,
                    "image_url": logo_image,
                }
                transform_result.append(product)

            return transform_result
