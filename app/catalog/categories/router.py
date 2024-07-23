from fastapi import APIRouter


router=APIRouter(
    prefix="/categories",
    tags=["Категории товаров"]
)

@router.get("")
def get_main_categories():
    pass

@router.get("/{parent_id}")
def get_subcategories(parent_id):
    pass