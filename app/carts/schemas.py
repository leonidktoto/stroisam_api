from pydantic import BaseModel


class SCarts(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: int
    sum_price: int
    user_id: int


class SItemProduct(BaseModel):
    product_id: int
    quantity: int


class SItemQuantityUpdate(BaseModel):
    quantity: int


class SUserCart(BaseModel):
    id: int
    product_id: int
    article: str | None
    product_name: str
    quantity: int
    price: int
    sum_price: int
    image_url: str | None
