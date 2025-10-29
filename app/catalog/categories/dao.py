from sqlalchemy import case, desc, distinct, func, select
from sqlalchemy.orm import aliased

from app.catalog.categories.models import Categories
from app.DAO.base import BaseDAO
from app.database import async_session_maker


class CategoriesDAO(BaseDAO):
    model = Categories

    @classmethod
    async def find_subcategory(cls, parent_id):
        async with async_session_maker() as session:
            cat = aliased(Categories)

            subquery = (
                select(
                    cat.parent_id, func.json_agg(distinct(cat.id)).label("children_id")
                ).group_by(cat.parent_id)
            ).subquery("children")

            # Прямо передаем условие в case
            query = (
                select(
                    Categories.id,
                    Categories.parent_id,
                    Categories.category_name,
                    Categories.image_url,
                    case(
                        (
                            subquery.c.children_id.isnot(None),
                            True,
                        ),  # Условие, если есть дочерние категории
                        else_=False,
                    ).label(
                        "has_children"
                    ),  # Логическое значение True/False
                )
                .select_from(Categories)
                .join(subquery, Categories.id == subquery.c.parent_id, isouter=True)
                .where(Categories.parent_id == parent_id)
                .order_by(Categories.category_name.asc())
            )

            result = await session.execute(query)
            return result.mappings().all()
