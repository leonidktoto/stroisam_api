from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel, EmailStr
from pydantic.json_schema import SkipJsonSchema
import random

from smsaero import SmsAeroException

from app.sms_aero import send_sms_api
from app.users.dao import UsersDAO
from app.users.models import Users
from app.exceptions import IncorrectSmsValidationException, SmsValidationExpired, UserAlreadyExistsException, UserIsBlocked, UserIsNotRegisteredException 
from app.users.auth import  send_sms
from app.users.sms_codes.dao import SmsCodesDAO
from app.users.sms_codes.models import SmsCodes



router=APIRouter(
    prefix="/Users",
    tags=["Auth & Пользователи"]
)




class SRegisterUser(BaseModel):

    first_name: int
    last_name: int | None
    phone: int
    email: EmailStr

def generate_sms_code():
    return str(random.randint(100000, 999999))



@router.get("/register")
async def register_user(
    first_name: Annotated[str, Query(max_length=15)],
    email: EmailStr,
    phone: Annotated[str, Query(regex=r'^\d{10}$', description="Номер телефона (ровно 10 цифр)", title='Строка')],
    last_name: Annotated[str | SkipJsonSchema[None], Query(max_length=15)] = None,
    ):
    user = await UsersDAO.find_one_or_none(phone=phone)
    if user:
        raise  UserAlreadyExistsException
    await UsersDAO.add_data(first_name=first_name, last_name=last_name, phone=phone, email=email)


@router.get("/sms_verification")
async def sms_verification(
    phone: Annotated[str, Query(regex=r'^\d{10}$', description="Номер телефона (ровно 10 цифр)", title='Строка')]):
    
    user: Optional[Users] = await UsersDAO.find_one_or_none(phone=phone)
    if not user:
        raise UserIsNotRegisteredException
    
    latest_smscode: Optional[SmsCodes] = await SmsCodesDAO.last_sms_code(user_id=user.id)

    if latest_smscode:
        current_utc_time=datetime.now(timezone.utc) #Текущее время в UTC
        expires_at_utc = latest_smscode.expires_at.replace(tzinfo=timezone.utc) #Добавляем временную зону к полученному времени
        time_difference = current_utc_time - expires_at_utc

        if user.registration_attempts >= 5 and time_difference < timedelta(hours=24):
            raise UserIsBlocked

        if expires_at_utc > current_utc_time:
            return {
                "status" : "wait",
                "time" : round((expires_at_utc-current_utc_time).total_seconds())
            }
        else:
            code=generate_sms_code()
            await SmsCodesDAO.add_data(user_id=user.id, code=code)
            #Добавить счетчик отправок смс 

            #Добавить через Celery
            try:
                result = send_sms_api(int(f'7{phone}'), code)
                return {
                "status" : result,
                "time" : 0
            }
            except SmsAeroException as e:
                print(f"An error occurred: {e}")



            






@router.get("/login")
async def login(
    phone: Annotated[str, Query(regex=r'^\d{10}$', description="Номер телефона (ровно 10 цифр)", title='Строка')],
    sms: Annotated[str, Query(max_length=8)]):

    user: Optional[Users] = await UsersDAO.find_one_or_none(phone=phone)
    if not user:
        raise UserIsNotRegisteredException

    sms_code: Optional[SmsCodes] = await SmsCodesDAO.last_sms_code(user_id=user.id)
    
    if sms_code:
        if sms_code.code!=sms:
            raise IncorrectSmsValidationException

        current_utc_time=datetime.now(timezone.utc) #Текущее время в UTC
        expires_at_utc = sms_code.expires_at.replace(tzinfo=timezone.utc) #Добавляем временную зону к полученному времени
        if expires_at_utc<current_utc_time:
            raise SmsValidationExpired
        
        await SmsCodesDAO.update_data(id=sms_code.id, is_used=True)
        #выдать токен
        #Обнулить попытки захода

        