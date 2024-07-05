import datetime
from sqlalchemy import ForeignKey, func, event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base




class Orders(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    order_date: Mapped[datetime.date]
    total_amount: Mapped[int]

""" # Это создание тригеров на автоматический подсчет total_amount
def update_order_total(mapper, connection, target):
    session = Session.object_session(target)
    order_id = target.order_id
    total = session.query(func.sum(OrderItems.price)).filter(OrderItems.order_id == order_id).scalar()
    
    session.query(Orders).filter(Orders.id == order_id).update({"total_amount": total})
    session.commit()

# Привязка событий к функциям
event.listen(OrderItems, 'after_insert', update_order_total)
event.listen(OrderItems, 'after_update', update_order_total)
"""