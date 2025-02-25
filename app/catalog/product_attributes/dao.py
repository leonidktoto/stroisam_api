from app.catalog.product_attributes.models import ProductAttributes
from app.DAO.base import BaseDAO


class ProductAttributesDAO(BaseDAO):
    model = ProductAttributes
