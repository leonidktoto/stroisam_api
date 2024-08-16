from app.DAO.base import BaseDAO
from app.orders.order_items.models import OrderItems


class OrdersItemsDAO(BaseDAO):
    model = OrderItems