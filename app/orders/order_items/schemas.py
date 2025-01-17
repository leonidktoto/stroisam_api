from pydantic import BaseModel

class SOrderItems(BaseModel):
    id: int
    product_id: int
    article: str | None
    product_name: str
    quantity: int
    price: int
    sum_price: int