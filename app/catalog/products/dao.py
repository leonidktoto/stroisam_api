
from app.DAO.base import BaseDAO
from app.catalog.products.models import Products
from app.database import async_session_maker
from sqlalchemy import select
from sqlalchemy.orm import selectinload, contains_eager
from app.catalog.product_images.models import ProductImages


class ProductsDAO(BaseDAO):
    model = Products

    @classmethod
    async def get_products_in_category(cls):
        async with async_session_maker() as session:
               # query = select(Products).options(
               #     selectinload(Products.image)
               # ).where(Products.category_id == 25)
               # result = await session.execute(query)
               # return result.mappings().all()
        # Подзапрос для фильтрации изображений с logo = True
            subquery = (
            select(ProductImages)
            .where(ProductImages.logo == True)
            .subquery()
            )

            # Основной запрос с присоединением подзапроса
            query = (
                select(Products)
                .join(subquery, Products.id == subquery.c.product_id, isouter=True)
                .options(contains_eager(Products.image, alias=subquery))
                .where(Products.category_id == 25)
            )

            result = await session.execute(query)
            #products = result.scalars().unique().all()
            return result.mappings().unique().all()

    @classmethod
    async def get_products_in_category2(cls, category_id: int):
        async with async_session_maker() as session:
            # Подзапрос для фильтрации изображений с logo = True
            subquery = (
                select(ProductImages.product_id, ProductImages.image_url)
                .where(ProductImages.logo == True)
                .subquery()
            )

            # Основной запрос с присоединением подзапроса
            query = (
                select(Products.id, Products.article, Products.product_name, Products.price, subquery.c.image_url)
                .join(subquery, Products.id == subquery.c.product_id, isouter=True)
                .where(Products.category_id == category_id)
            )

            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_products_in_category3(cls):
        async with async_session_maker() as session:
            # Подзапрос для фильтрации изображений с logo = True
            subquery = (
                select(ProductImages)
                .where(ProductImages.logo == True)
                .subquery()
            )

            # Основной запрос с присоединением подзапроса
            query = (
                select(Products.article, Products.product_name)
                .join(subquery, Products.id == subquery.c.product_id, isouter=True)
                .options(contains_eager(Products.image, alias=subquery))
                .where(Products.category_id == 25)
            )

            result = await session.execute(query)
            return result.all()

    @classmethod
    async def get_products_in_category4(cls):
        async with async_session_maker() as session:
            # Подзапрос для фильтрации изображений с logo = True
            subquery = (
                select(ProductImages)
                #.where(ProductImages.logo == True)
                .subquery()
            )
            cte=(select(Products.id,Products.product_name, Products.image).filter_by(category_id=25)).cte("products_filtered")

            # Основной запрос с присоединением подзапроса
            query = (
            select(cte.c.id, cte.c.product_name, subquery.c.image_url)
            .outerjoin(subquery, cte.c.id == subquery.c.product_id)
            )


            result = await session.execute(query)
            return result.mappings().unique().all()