
from app.DAO.base import BaseDAO
from app.catalog.attributes.models import Attributes
from app.catalog.product_attributes.models import ProductAttributes
from app.catalog.products.models import Products
from app.database import async_session_maker
from sqlalchemy import alias, and_, distinct, func, or_, select
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager
from app.catalog.product_images.models import ProductImages
from fastapi.encoders import jsonable_encoder


class ProductsDAO(BaseDAO):
    model = Products

    @classmethod
    async def find_products_by_category_id(cls, category_id: int):
        async with async_session_maker() as session:
            # Подзапрос для фильтрации изображений с logo = True
            subquery = (
                select(ProductImages.product_id, ProductImages.image_url)
                .where(ProductImages.logo == True)
                .subquery()
            )

            # Основной запрос с присоединением подзапроса
            query = (
                select(
                    Products.id, 
                    Products.article, 
                    Products.category_id, 
                    Products.product_name, 
                    Products.description, 
                    Products.price, 
                    Products.stock, 
                    subquery.c.image_url)
                .join(subquery, Products.id == subquery.c.product_id, isouter=True)
                .where(Products.category_id == category_id)
            )

            result = await session.execute(query)
            return result.mappings().all()




    @classmethod
    async def find_products_by_id(cls, id: int):
        async with async_session_maker() as session:

            query = (
            select(Products)
                .options(
                    joinedload(Products.product_attribute).joinedload(ProductAttributes.attribute_name),
                    joinedload(Products.image)
                    )
                    .where(Products.id == id)
            )           
            result = await session.execute(query)    
            result = result.scalar()

            if result is None:
                return None 

            transform_result={
                "id" : result.id,
                "article" : result.article,
                "category_id" : result.category_id,
                "product_name": result.product_name,
                "description" : result.description,
                "price" : result.price,
                "stock" : result.stock,
                "product_attributes" : [],
                "image_urls" : [],
            }
            for attr in result.product_attribute:
                transform_result["product_attributes"].append({
                    "attribute_name" : attr.attribute_name.attribute_name,
                    "attribute.value" : attr.attribute_value,
                })
            for attr in result.image:
                transform_result["image_urls"].append(attr.image_url)
            return transform_result


    @classmethod
    async def find_products_by_filter(cls, filters, category_id: int):
        async with async_session_maker() as session:

            attr = aliased(Attributes)
            pr_attr = aliased(ProductAttributes)
            im = aliased(ProductImages)
            pr = aliased(Products)
            # Подзапрос для фильтрации изображений с logo = True
            subquery_pr_attr = (
                select(
                    pr_attr.product_id,
                    attr.attribute_name,
                    pr_attr.attribute_value,
                )
                .select_from(pr_attr)
                .join(attr, pr_attr.attribute_name_id == attr.id, isouter=True)
                .subquery("a")
                
            )
            subquery_im = (
                select(im.product_id, im.image_url)
                .where(im.logo == True)
                .subquery("im")
            )
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            filters = jsonable_encoder(filters)
            print(filters)
   #         filters = [
   #
   # {'attribute_name': 'Размер', 'attribute_value': ["25x35x2000 мм"]},
   # {'attribute_name': 'Сорт', 'attribute_value': ["Оптима"]},
   #         ]

            filter_conditions = []
            for filter_item in filters:
                attribute_name = filter_item['attribute_name']
                attribute_values = filter_item['attribute_value']
                condition = and_(
                    subquery_pr_attr.c.attribute_name == attribute_name,
                    subquery_pr_attr.c.attribute_value.in_(attribute_values)
                )
                filter_conditions.append(condition)

            subquery_pr = (
                select(
                    subquery_pr_attr.c.product_id,
                    func.count(subquery_pr_attr.c.product_id).label('count_product')
                )
                .filter(or_(*filter_conditions))  # Применяем фильтры
                .group_by(subquery_pr_attr.c.product_id)
                .having(func.count(subquery_pr_attr.c.product_id) == len(filters))  # Проверяем совпадение всех фильтров
                .subquery("find_pr")
            )
            
            query=(
                select(
                    Products.id, 
                    Products.article, 
                    Products.category_id, 
                    Products.product_name, 
                    Products.description, 
                    Products.price, 
                    Products.stock, 
                    subquery_im.c.image_url,
                )
                .join(subquery_pr, Products.id == subquery_pr.c.product_id)
                .join(subquery_im, Products.id == subquery_im.c.product_id, isouter=True)
                .where(Products.category_id == category_id)         
            )
  
            print("!!!!!!@@@@@@@@@@!!!!!!!!!!@@@@@@@@@@@@!!!!!!!!!!!")
            print(query.compile(compile_kwargs={"literal_binds": True}))
            result = await session.execute(query)
            return result.mappings().all()