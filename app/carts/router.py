from fastapi import APIRouter, Depends, Response

from app.carts.dao import CartsDAO
from app.carts.schemas import SItemProduct, SUserCart
from app.catalog.products.dao import ProductsDAO
from app.exceptions import CannotAddDataToDatabase, CannotAddUpdateDatabase
from app.users.schemas import SUsers
from app.users.validation import get_current_active_auth_user

router = APIRouter(
    prefix="/users/cart",
    tags=["Корзина"],
    # dependencies=[Depends(http_bearer)]
)


@router.get("/", response_model=list[SUserCart] | None)
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

    # Проверяем если есть в корзине то обновляем количество и цену товара, если нет добавляем товар.
    product_in_cart = await CartsDAO.find_one_or_none(product_id=items.product_id, user_id=user.id)
    if product_in_cart:
        quantity = items.quantity + product_in_cart.quantity
        await CartsDAO.update_data(
            {
                "quantity": quantity,
                "price": product.price,
            },
            product_id=items.product_id,
            user_id=user.id,
        )
        message = "Обновлено количество товара в корзине"

    else:
        quantity = items.quantity
        await CartsDAO.add_data(
            product_id=product.id, quantity=quantity, price=product.price, user_id=user.id
        )
        message = "Товар добавлен в корзину"

    return {"message": message, "product_id": items.product_id, "quantity": quantity}


@router.patch("/items")
async def partial_update_item(
    items: SItemProduct,
    user: SUsers = Depends(get_current_active_auth_user),
):
    product = await ProductsDAO.find_one_or_none(id=items.product_id)
    if not product:
        raise CannotAddDataToDatabase
    product_in_cart = await CartsDAO.find_one_or_none(product_id=items.product_id, user_id=user.id)

    if not product_in_cart:
        raise CannotAddUpdateDatabase

    await CartsDAO.update_data(
        {
            "quantity": items.quantity,
            "price": product.price,
        },
        product_id=items.product_id,
        user_id=user.id,
    )

    return {
        "message": "Обновлено количество товара в корзине",
        "product_id": items.product_id,
        "quantity": items.quantity,
    }


@router.delete("/items/{id}")
async def remove_item_from_cart(
    id: int,
    user: SUsers = Depends(get_current_active_auth_user),
):
    await CartsDAO.delete_by_filter(id=id, user_id=user.id)
    return Response(status_code=204)


@router.delete("/items")
async def clear_cart(
    user: SUsers = Depends(get_current_active_auth_user),
):
    await CartsDAO.delete_by_filter(user_id=user.id)
    return Response(status_code=204)
