from app.DAO.base import BaseDAO
from app.catalog.product_images.models import ProductImages

class ProductImagesDAO(BaseDAO):
    model = ProductImages