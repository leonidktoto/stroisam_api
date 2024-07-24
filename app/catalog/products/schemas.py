from pydantic import BaseModel
#from app.catalog.product_images.schemas import SProductImages
from typing import List

class SProducts(BaseModel):
    id: int
    article: int
    category_id: int
    product_name: str
    description: str
    price: int
    stock: int

    class ConfigDict:
        from_attributes = True
    

class SProductsByCategoryId(BaseModel):
    id: int
    article: int
    product_name: str
    price: int
    image_url: str | None