from pydantic import BaseModel

class SProductImages(BaseModel):
    id: int
    product_id: int
    description: str
    logo: bool
    image_url: str