from app.catalog.product_images.models import ProductImages
from app.DAO.base import BaseDAO


class ProductImagesDAO(BaseDAO):
    model = ProductImages
