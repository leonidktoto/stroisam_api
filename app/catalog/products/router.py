from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from app.catalog.products.dao import ProductsDAO
from app.catalog.products.schemas import  SProduct, SProductsWithAttr


router=APIRouter(
    prefix="/products",
    tags=["Товары"]
)

class FilterProduct(BaseModel):
    attribute_name: str 
    attribute_value: list[str] 



@router.get("/category/{category_id}" , response_model=list[SProduct])
async def get_products_by_category_id(category_id: int):
    result = await ProductsDAO.find_products_by_category_id(category_id=category_id)
    return result

@router.get("/id/{id}", response_model=SProductsWithAttr | None)
async def get_products_by_id(id:int):
    result = await ProductsDAO.find_products_by_id(id)
    return result

@router.post("/filter", response_model=list[SProduct])
async def get_test(filters: list[FilterProduct], category_id: int):
    result = await ProductsDAO.test(filters, category_id)
    return result