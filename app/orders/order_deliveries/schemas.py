from typing import Optional
from datetime import date
from pydantic import BaseModel, Field



class SOrder_delveries(BaseModel):
    id: int
    order_id: int
    desired_delivery_at: date 
    country: str
    city: str
    address: str 
    recipient_name: str
    phone_primary: str
    phone_secondary: str
    extra_info: str
    
class SOrder_delveries_request(BaseModel):
    desired_delivery_at: date = Field(..., description="Желаемая дата доставки")
    country: str = Field(..., max_length=56, description="Страна доставки")
    city: str = Field(..., max_length=100, description="Город доставки")
    address: str = Field(..., max_length=255, description="Адрес доставки")
    recipient_name: Optional[str] = Field(None, max_length=100, description="ФИО получателя")
    phone_primary: Optional[str] = Field(None, max_length=15, description="Основной телефон")
    phone_secondary: Optional[str] = Field(None, max_length=15, description="Дополнительный телефон")
    extra_info: Optional[str] = Field(None, max_length=500, description="Комментарий к заказу")

