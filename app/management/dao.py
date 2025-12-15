from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.catalog.products.models import Products
from app.orders.models import Orders
from app.orders.order_deliveries.models import OrderDeliveries
from app.orders.order_items.models import OrderItems
from app.users.models import Users
from sqlalchemy import select


class ManagementDAO(BaseDAO):
    @staticmethod
    async def find_order(
        order_id=None,
    ):
        async with async_session_maker() as session:
            query = (
            select(
                Users.first_name,
                Users.last_name,
                Users.phone.label("user_phone"),
                Users.email,

                Orders.id,
                Orders.order_status,
                Orders.order_date,
                Orders.total_amount,
                
                OrderDeliveries.desired_delivery_at,
                (OrderDeliveries.city + ", " + OrderDeliveries.address).label("delivery_address"),
                OrderDeliveries.recipient_name,
                OrderDeliveries.phone_primary,
                OrderDeliveries.phone_secondary,
                OrderDeliveries.extra_info,

                Products.id,
                Products.product_name,
                OrderItems.product_id,
                OrderItems.quantity,
                OrderItems.price,
                OrderItems.sum_price,
            )
            .join(OrderItems, OrderItems.order_id == Orders.id, isouter=True)
            .join(Products, OrderItems.product_id == Products.id, isouter=True)
            .join(Users, Orders.user_id == Users.id, isouter=True)
            .join(OrderDeliveries, OrderDeliveries.order_id == Orders.id, isouter=True)
            .where(Orders.id == order_id)
            .order_by(OrderItems.id)
            )
            rows = (await session.execute(query)).all()

            if not rows:
                return None

            # первая строка (общие данные)
            r0 = rows[0]

            # user
            user = {
                "first_name": r0.first_name,
                "last_name": r0.last_name,
                "phone": r0.user_phone,
                "email": r0.email,
            }

            # delivery
            delivery = {
                "desired_delivery_at": r0.desired_delivery_at,
                "address": r0.delivery_address,
                "recipient_name": r0.recipient_name,
                "phone_primary": r0.phone_primary,
                "phone_secondary": r0.phone_secondary,
                "extra_info": r0.extra_info,
            }

            # items
            items = []
            for r in rows:
                items.append({
                    "product_id": r.product_id,
                    "product_name": r.product_name,
                    "quantity": r.quantity,
                    "price": r.price,
                    "sum_price": r.sum_price,
                })

            # итоговый объект
            order_full = {
                "order_id": r0.id,
                "order_status": r0.order_status,
                "order_date": r0.order_date.isoformat() if hasattr(r0.order_date, "isoformat") else r0.order_date,
                "user": user,
                "delivery": delivery,
                "items": items,
                "total_amount": r0.total_amount,
            }

            return order_full  