from pydantic import BaseModel


class SUserFavorite(BaseModel):
    id: int
    product_id: int
    article: str | None
    product_name: str
    image_url: str | None

class SItemProduct(BaseModel):
    product_id: int