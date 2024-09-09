from fastapi import APIRouter, Depends, Response

from app.carts.dao import CartsDAO
from app.carts.model import Carts
from app.carts.schemas import SItemProduct, SItemQuantityUpdate, SUserCart
from app.catalog.products.dao import ProductsDAO
from app.exceptions import CannotAddDataToDatabase
from app.users.schemas import SUsers
from app.users.validation import get_current_active_auth_user
from app.users.router import http_bearer


router=APIRouter(
    prefix="/user/cart",
    tags=["Корзина"],
    dependencies=[Depends(http_bearer)]
)
"""
	•	POST /cart/{user_id} — Добавление товара в корзину пользователя.
	•	GET /cart/{user_id} — Получение содержимого корзины.
	•	POST /order/{user_id} — Создание заказа на основе содержимого корзины.
	•	GET /order/{order_id} — Получение информации о заказе.
	•	DELETE /cart/{user_id}/item/{item_id} — Удаление товара из корзины.

"""

@router.get("/", response_model= list[SUserCart])
async def get_cart_contents(
    user: SUsers = Depends(get_current_active_auth_user),
    ):
    cart = await CartsDAO.get_user_cart(user.id)
    return cart


@router.post("/items")
async def add_item_to_cart(
    items: SItemProduct,
    user: SUsers = Depends(get_current_active_auth_user),
    ):
    product = await ProductsDAO.find_one_or_none(id=items.product_id)
    if not product:
        raise CannotAddDataToDatabase
    
    #Проверяем если есть в корзине то обновляем количество и цену товара, если нет добавляем товар.
    product_in_cart = await CartsDAO.find_one_or_none(product_id=items.product_id, user_id=user.id)
    if product_in_cart: 
         await CartsDAO.update_data(
            {
                "quantity":items.quantity+product_in_cart.quantity,
                "price":product.price,
            },
            product_id=items.product_id, 
            user_id=user.id,
            )
    else:
        await CartsDAO.add_data(
            product_id = product.id, 
            quantity = items.quantity,
            price = product.price,
            user_id = user.id)
        
    return Response(status_code=200)

@router.patch("/items/{item_id}")
async def partial_update_item(
    item_id: int, 
    quantity: SItemQuantityUpdate,
    user: SUsers = Depends(get_current_active_auth_user),
    ):
    # Логика частичного обновления товара
    return {"message": f"Item partially updated {quantity} "}

@router.delete("/items/{item_id}")
async def remove_item_from_cart(
    item_id: int,
    user: SUsers = Depends(get_current_active_auth_user),
    ):
    return {"message": f"Deleted items {item_id} "}