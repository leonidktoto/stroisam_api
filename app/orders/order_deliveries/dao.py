from app.orders.order_deliveries.models import OrderDeliveries
from app.DAO.base import BaseDAO


class OrderDeliveriesDAO(BaseDAO):
    model = OrderDeliveries