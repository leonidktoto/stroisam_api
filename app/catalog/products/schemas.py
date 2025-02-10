from pydantic import BaseModel, Field
#from app.catalog.product_images.schemas import SProductImages
from typing import List

class SProducts(BaseModel):
    id: int
    article: str | None
    category_id: int
    product_name: str
    description: str | None
    price: int
    stock: int

    class ConfigDict:
        from_attributes = True
    

class SProduct(SProducts):
    category_id: int = Field(exclude=True)
    stock: int = Field(exclude=True)
    description: str | None = Field(exclude=True)
    image_url: str | None

class SProductsWithAttr(SProducts):
    category_id: int = Field(exclude=True)
    stock: int = Field(exclude=True)
    product_attributes: list[dict | None]
    image_urls: list[str | None]

class SAttributeValues(BaseModel):
    attribute_name: str
    attribute_value: List[str]

class SProduct_name(BaseModel):
    product_name: str