from typing import List
from fastapi import APIRouter
from app.catalog.categories.dao import CategoriesDAO
from app.catalog.categories.schemas import SCategories

router=APIRouter(
    prefix="/categories",
    tags=["Категории товаров"]
)

@router.get("/main", response_model=list[SCategories])
async def get_main_categories():
    main_catalog = await CategoriesDAO.find_all(parent_id=None)
    return main_catalog

@router.get("/sub/{parent_id}", response_model=list[SCategories])
async def get_subcategories(parent_id: int):
    main_catalog = await CategoriesDAO.find_all(parent_id=parent_id)
    return main_catalog