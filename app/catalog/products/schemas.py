from pydantic import BaseModel, Field
#from app.catalog.product_images.schemas import SProductImages
from typing import List

class SProducts(BaseModel):
    id: int
    article: str | None
    category_id: int
    product_name: str
    description: str
    price: int
    stock: int

    class ConfigDict:
        from_attributes = True
    

class SProduct(SProducts):
    category_id: int = Field(exclude=True)
    stock: int = Field(exclude=True)
    description: str = Field(exclude=True)
    image_url: str | None

class SProductsWithAttr(SProducts):
    category_id: int = Field(exclude=True)
    stock: int = Field(exclude=True)
    product_attributes: list[dict | None]
    image_urls: list[str | None]

