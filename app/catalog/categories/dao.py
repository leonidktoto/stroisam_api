from app.DAO.base import BaseDAO
from app.catalog.categories.models import Categories

class CategoriesDAO(BaseDAO):
    model = Categories
