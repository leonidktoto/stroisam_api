from datetime import date
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query, Response
from pydantic.json_schema import SkipJsonSchema

from app.carts.dao import CartsDAO
from app.exceptions import CartIsEmpty, OrderNotCanceled, OrderNumError
from app.orders.dao import OrdersDAO
from app.orders.models import OrderStatus
from app.orders.order_items.dao import OrdersItemsDAO
from app.orders.order_items.models import OrderItems
from app.orders.order_items.schemas import SOrderItems
from app.orders.schemas import SOrdersWithoutUserId
from app.users.schemas import SUsers
from app.users.validation import get_current_active_auth_user
from app.users.router import http_bearer


router=APIRouter(
    prefix="/users/orders",
    tags=["Заказы"],
    #dependencies=[Depends(http_bearer)]
)

@router.get("", response_model = list[SOrdersWithoutUserId])
async def get_user_orders(
    user: SUsers = Depends(get_current_active_auth_user),
    start_date: Optional[date] = Query(None, description="Фильтровать заказы начиная с этой даты"),
    end_date: Optional[date] = Query(None, description="Фильтровать заказы до этой даты"),
    status: Optional[OrderStatus] = Query(None, description="Фильтровать по статусу заказа"),
    ):
    
    return await OrdersDAO.find_user_orders(
        user_id = user.id, 
        start_date = start_date,
        end_date = end_date,
        status = status,
    )

@router.post("/checkout", )
async def create_order(
    user: SUsers = Depends(get_current_active_auth_user),
    ):
    cart_items = await CartsDAO.get_user_cart(user.id)
    if not cart_items:
        raise CartIsEmpty 
    order_id = await OrdersDAO.add_data(user_id = user.id)

    for item in cart_items:
        await OrdersItemsDAO.add_data(
            order_id = order_id["id"], 
            product_id = item["product_id"],
            quantity = item["quantity"],
            price = item["price"],
        )
    await CartsDAO.delete_by_filter(user_id = user.id) # очистка корзины
    # здесь нужно передать в celery id для передачи заказа менеджеру
    return {"message": "Заказ создан", "order_id": order_id["id"]}

        
@router.get("/{order_id}", response_model=SOrderItems)
async def get_order_detail(
    order_id: int,
    user: SUsers = Depends(get_current_active_auth_user),       
):
    if not await OrdersDAO.find_one_or_none(id = order_id, user_id = user.id):
        raise OrderNumError
    return await OrdersItemsDAO.detail_order(order_id=order_id)

@router.post("/{order_id}/cancel", response_model=SOrdersWithoutUserId)
async def cancel_order(
    order_id: int,
    user: SUsers = Depends(get_current_active_auth_user),       
):
    order = await OrdersDAO.find_one_or_none(id = order_id, user_id = user.id)
    if not order:
        raise OrderNotCanceled
    if order.order_status in [
        OrderStatus.AWAITING_PAYMENT,
        OrderStatus.PAID,
        OrderStatus.COMPLETED,
        OrderStatus.CANCELED,
    ]:
        raise OrderNotCanceled
    return await OrdersDAO.update_data({"order_status":OrderStatus.CANCELED}, user_id = user.id, id = order_id)

@router.post("/{order_id}/reorder")
async def reorder(
    order_id: int, 
    user: SUsers = Depends(get_current_active_auth_user)
):
    order = await OrdersDAO.find_one_or_none(id = order_id, user_id = user.id)
    if not order:
        raise OrderNumError

    order_items = await OrdersItemsDAO.detail_order(order_id=order_id)
    if not order_items:
        raise OrderNumError
    
    for item in order_items:
        await CartsDAO.add_data( 
            product_id = item["product_id"],
            quantity = item["quantity"],
            user_id = user.id,
        )

    return {"message": "Товары заказа добавлены в корзину"}