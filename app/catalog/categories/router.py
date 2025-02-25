from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.catalog.categories.dao import CategoriesDAO
from app.catalog.categories.schemas import SCategoriesWithChldrn

router = APIRouter(prefix="/categories", tags=["Категории товаров"])


@router.get("/main", response_model=list[SCategoriesWithChldrn])
@cache(expire=60)
async def get_main_categories():
    main_catalog = await CategoriesDAO.find_subcategory(None)
    return main_catalog


@router.get("/sub/{parent_id}", response_model=list[SCategoriesWithChldrn])
@cache(expire=60)
async def get_subcategories(parent_id: int):
    catalog = await CategoriesDAO.find_subcategory(parent_id)
    return catalog
