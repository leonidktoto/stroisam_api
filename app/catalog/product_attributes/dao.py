from app.DAO.base import BaseDAO
from app.catalog.product_attributes.models import ProductAttributes

class ProductAttributesDAO(BaseDAO):
    model = ProductAttributes
