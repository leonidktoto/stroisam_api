from typing import List
from fastapi import APIRouter

from app.catalog.products.dao import ProductsDAO
from app.catalog.products.schemas import  SProductsByCategoryId


router=APIRouter(
    prefix="/products",
    tags=["Товары"]
)

@router.get("/category/{category_id}" , response_model=list[SProductsByCategoryId])
async def get_products(category_id: int):
    result = await ProductsDAO.get_products_in_category2(category_id=category_id)
    return result

