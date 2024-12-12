from datetime import datetime, timedelta, timezone
import random
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query, Response
from pydantic import EmailStr
from pydantic.json_schema import SkipJsonSchema

from smsaero import SmsAeroException

from app.users.helpers import generate_sms_code, send_new_sms_code
from app.config import Settings_env
from app.sms_aero import send_sms_api
from app.users.dao import UsersDAO
from app.users.models import Users
from app.exceptions import (
    UserAlreadyExistsException, 
    UserIsBlocked, 
    UserIsNotRegisteredException,
    ) 

from app.users.schemas import SRegisterUser, STokenInfo, SUserAuth, SUsers, SUsersPhone
from app.users.sms_codes.dao import SmsCodesDAO
from app.users.sms_codes.models import SmsCodes

from fastapi.security import (
    HTTPBearer,
    )
from app.users.token import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, auth_user_set_cookie, create_access_token, create_refresh_token
from app.users.validation import (
    get_current_active_auth_user, 
    get_current_token_payload,
    get_current_token_payload_with_type, 
    validate_auth_user, 
    get_current_auth_user_refresh,
    )
from app.config import settings
from app.tasks.tasks import send_sms_message

http_bearer = HTTPBearer(auto_error=False)


router=APIRouter(
    prefix="/users",
    tags=["Auth & Пользователи"],
   # dependencies=[Depends(http_bearer)]
)





@router.post("/register")
async def register_user(
    reg_user: SRegisterUser
    ):
    user = await UsersDAO.find_one_or_none(phone=reg_user.phone)
    if user:
        raise  UserAlreadyExistsException
    await UsersDAO.add_data(first_name=reg_user.first_name, last_name=reg_user.last_name, phone=reg_user.phone, email=reg_user.email)


@router.post("/sms_verification") #Переписать!!! Разделить на функции, добавить else latest_sms_code
async def sms_verification(user_phone: SUsersPhone):
    phone=user_phone.phone
    print(phone)
    user = await UsersDAO.find_one_or_none(phone=phone)
    if not user:
        raise UserIsNotRegisteredException
    
    latest_smscode = await SmsCodesDAO.last_sms_code(user_id=user.id)

    if latest_smscode:
        current_utc_time=datetime.now(timezone.utc) #Текущее время в UTC
        expires_at_utc = latest_smscode.expires_at.replace(tzinfo=timezone.utc) #Добавляем временную зону к полученному времени
        time_difference = current_utc_time - expires_at_utc

        # Проверка на блокировку пользователя
        if user.registration_attempts >= 5 and time_difference < timedelta(hours=24):
            raise UserIsBlocked
            
        # Проверка, если смс-код ещё действителен
        if expires_at_utc > current_utc_time:
            return {
                "status" : "wait",
                "time" : round((expires_at_utc-current_utc_time).total_seconds())
            }

    return await send_new_sms_code(user, phone)
        


@router.post("/login/", response_model=STokenInfo)
async def login(
    response: Response,
    user: SUserAuth = Depends(validate_auth_user) 
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    auth_user_set_cookie(response, ACCESS_TOKEN_TYPE, access_token)
    auth_user_set_cookie(response, REFRESH_TOKEN_TYPE, refresh_token)

    return STokenInfo(
        access_token = access_token,
        refresh_token = refresh_token
    )

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(ACCESS_TOKEN_TYPE)
    response.delete_cookie(REFRESH_TOKEN_TYPE)
    
@router.post("/refresh/", response_model = STokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(
    response: Response,
    user: SUsers = Depends(get_current_auth_user_refresh)
):
    access_token = create_access_token(user)
    auth_user_set_cookie(response, ACCESS_TOKEN_TYPE, access_token)


    return STokenInfo(
        access_token=access_token
    )


@router.get("/me/", response_model=SUserAuth)
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload_with_type(ACCESS_TOKEN_TYPE)),
    user: SUsers = Depends(get_current_active_auth_user)
):
    iat=payload.get("iat")
    print(iat)
    return user