from fastapi import APIRouter


router=APIRouter(
    prefix="/products",
    tags=["Товары"]
)

@router.get("/{category_id}")
def get_products(category_id):
    pass

