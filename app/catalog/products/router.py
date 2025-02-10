from typing import List
from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.catalog.products.dao import ProductsDAO
from app.catalog.products.schemas import  SAttributeValues, SProduct, SProduct_name, SProductsWithAttr
from fastapi_cache.decorator import cache


router=APIRouter(
    prefix="/products",
    tags=["Товары"]
)

class FilterProduct(BaseModel):
    attribute_name: str 
    attribute_value: list[str] 



@router.get("/category/{category_id}" , response_model=list[SProduct])
@cache(expire=60)
async def get_products_by_category_id(category_id: int):
    result = await ProductsDAO.find_products(category_id=category_id)
    return result

@router.get("/id/{id}", response_model=SProductsWithAttr | None)
async def get_products_by_id(id:int):
    result = await ProductsDAO.find_products_by_id(id)
    return result

@router.post("/filter", response_model=list[SProduct])
async def get_product_by_filter(filters: list[FilterProduct], category_id: int):
    result = await ProductsDAO.find_products_by_filter(filters, category_id)
    return result

@router.get("/filters/options", response_model=list[SAttributeValues])
async def get_filter_options(category_id: int):
    result = await ProductsDAO.get_filter_options(category_id)
    return result

@router.get("/search", response_model=List[SProduct])
@cache(expire=60)
async def search_products(
    search: str = Query(..., min_length=2, description="Поисковый запрос")
):
    result = await ProductsDAO.find_products(search=search)
    return result

@router.get("/autocomplete", response_model=List[SProduct_name])
async def autocomplete(
    search: str = Query(..., min_length=2, description="Текст для автодополнения"),
):
    result = await ProductsDAO.get_autocomplete(search=search)
    return result