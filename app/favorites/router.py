from fastapi import APIRouter, Depends, Response

from app.favorites.dao import FavoritesDAO
from app.favorites.schemas import SItemProduct, SUserFavorite
from app.catalog.products.dao import ProductsDAO
from app.exceptions import CannotAddDataToDatabase
from app.users.schemas import SUsers
from app.users.validation import get_current_active_auth_user

router = APIRouter(
    prefix="/users/favorites",
    tags=["Избранное"],
    # dependencies=[Depends(http_bearer)]
)


@router.get("/", response_model=list[SUserFavorite] | None)
async def get_favorites_contents(
    user: SUsers = Depends(get_current_active_auth_user),
):
    cart = await FavoritesDAO.get_user_cart(user.id)
    return cart


@router.post("/items")
async def add_item_to_cart(
    items: SItemProduct,
    user: SUsers = Depends(get_current_active_auth_user),
):
    product = await ProductsDAO.find_one_or_none(id=items.product_id)
    if not product:
        raise CannotAddDataToDatabase

    # Проверяем если нет в избранном то добавляем товар.
    product_in_cart = await FavoritesDAO.find_one_or_none(product_id=items.product_id, user_id=user.id)
    if not product_in_cart:
        await FavoritesDAO.add_data(
            product_id=product.id, user_id=user.id
        )
        message = "Товар добавлен в избранное"

        return {"message": message, "product_id": items.product_id}
    else:
        return {"message": "Товар уже в избранном"}






@router.delete("/items/{id}")
async def remove_item_from_favorites(
    id: int,
    user: SUsers = Depends(get_current_active_auth_user),
):
    await FavoritesDAO.delete_by_filter(id=id, user_id=user.id)
    return Response(status_code=204)


