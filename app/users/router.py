from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr
from pydantic.json_schema import SkipJsonSchema
import random
from smsaero import SmsAeroException

from app.sms_aero import send_sms_api
from app.users.dao import UsersDAO
from app.users.models import Users
from app.exceptions import (
    UserAlreadyExistsException, 
    UserIsBlocked, 
    UserIsNotRegisteredException,
    ) 

from app.users.schemas import STokenInfo, SUserAuth, SUsers
from app.users.sms_codes.dao import SmsCodesDAO
from app.users.sms_codes.models import SmsCodes

from fastapi.security import (
    HTTPBearer,
    )
from app.users.token import create_access_token, create_refresh_token
from app.users.validation import (
    get_current_active_auth_user, 
    get_current_token_payload, 
    validate_auth_user, 
    get_current_auth_user_refresh,
    )


http_bearer = HTTPBearer(auto_error=False)


router=APIRouter(
    prefix="/users",
    tags=["Auth & Пользователи"],
    dependencies=[Depends(http_bearer)]
)






def generate_sms_code():
    return str(random.randint(100000, 999999))




@router.post("/register")
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


@router.get("/sms_verification") #Переписать!!! Разделить на функции, добавить else latest_sms_code
async def sms_verification(
    phone: Annotated[str, Query(regex=r'^\d{10}$', description="Номер телефона (ровно 10 цифр)", title='Строка')]):
    
    user = await UsersDAO.find_one_or_none(phone=phone)
    if not user:
        raise UserIsNotRegisteredException
    
    latest_smscode = await SmsCodesDAO.last_sms_code(user_id=user.id)

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


@router.post("/login/", response_model=STokenInfo)
async def login(
    user: SUserAuth = Depends(validate_auth_user) ):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return STokenInfo(
        access_token = access_token,
        refresh_token = refresh_token
    )

@router.post("/refresh/")# response_model = STokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(
    user: SUsers = Depends(get_current_auth_user_refresh)
):
    access_token = create_access_token(user)
    return STokenInfo(
        access_token=access_token
    )


@router.get("/me/", response_model=SUserAuth)
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: SUsers = Depends(get_current_active_auth_user)
):
    iat=payload.get("iat")
    print(iat)
    return user