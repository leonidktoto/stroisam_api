from pydantic import BaseModel

class SCarts(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: int | None
    sum_price: int | None
    user_id: int

class SItemProduct(BaseModel):
    product_id: int
    quantity: int

class SItemQuantityUpdate(BaseModel):
    quantity: int

class SUserCart(BaseModel):
    id: int
    product_id: int
    article: int
    product_name: str
    quantity: int
    price: int
    sum_price: int

    