from datetime import date
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query, Response
from pydantic.json_schema import SkipJsonSchema

from app.carts.dao import CartsDAO
from app.exceptions import CartIsEmpty
from app.orders.dao import OrdersDAO
from app.orders.models import OrderStatus
from app.orders.order_items.dao import OrdersItemsDAO
from app.orders.order_items.models import OrderItems
from app.orders.schemas import SOrdersWithoutUserId
from app.users.schemas import SUsers
from app.users.validation import get_current_active_auth_user
from app.users.router import http_bearer


router=APIRouter(
    prefix="/users/orders",
    tags=["Заказы"],
    dependencies=[Depends(http_bearer)]
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

    # здесь нужно передать в celery id для передачи заказа менеджеру
    return {"message": "Заказ создан", "order_id": order_id["id"]}

        
@router.get("/detail/{order_id}")
async def get_order_detail(
    order_id: int,
    user: SUsers = Depends(get_current_active_auth_user),       
):
    return await OrdersItemsDAO.find_all(order_id=order_id)
