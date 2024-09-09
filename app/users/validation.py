
from datetime import datetime, timezone
from typing import Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from app.exceptions import IncorrectSmsValidationException, IncorrectTokenFormatException, InvalidToken, InvalidTokenType, SmsValidationExpired, UserInActive, UserIsNotRegisteredException
from app.users import auth
from app.users.schemas import SUserAuth, SUsers
from app.users.models import Users
from app.users.dao import UsersDAO
from fastapi import Form
from app.users.sms_codes.models import SmsCodes
from app.users.sms_codes.dao import SmsCodesDAO
from app.users.token import (
    TOKEN_TYPE_FIELD, 
    ACCESS_TOKEN_TYPE, 
    REFRESH_TOKEN_TYPE
    )
    
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/users/login/")


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
) -> SUsers:
    user: Optional[Users] = await UsersDAO.find_one_or_none(phone=username)
    if not user:
        raise UserIsNotRegisteredException

    sms_code: Optional[SmsCodes] = await SmsCodesDAO.last_sms_code(user_id=user.id)
       
    if not sms_code:
        raise IncorrectSmsValidationException
    if sms_code.code!=password:
        raise IncorrectSmsValidationException

    current_utc_time=datetime.now(timezone.utc) #Текущее время в UTC
    expires_at_utc = sms_code.expires_at.replace(tzinfo=timezone.utc) #Добавляем временную зону к полученному времени
    if expires_at_utc<current_utc_time:
        raise SmsValidationExpired
        
    await SmsCodesDAO.update_data({"is_used":True}, id=sms_code.id)
    if not user.is_active:
        raise UserInActive
    #Обнулить попытки захода
    return user

def get_current_token_payload(
    token: str = Depends(oauth2_scheme)
) -> dict:
    try:
        payload = auth.decode_jwt(token)
    except InvalidTokenError as e:
        raise IncorrectTokenFormatException
    return payload


async def get_user_by_token_sub(payload: dict) -> SUserAuth:
    username: str | None = payload.get("sub")
    user: Optional[Users] = await UsersDAO.find_one_or_none(phone=username)
    if not user:
        raise UserIsNotRegisteredException
    return user

def validate_token_type(
    payload: dict, 
    token_type: str
    ) -> bool:
    curent_token_type=payload.get(TOKEN_TYPE_FIELD)
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise InvalidToken(detail=f"Неверный тип токена {curent_token_type!r} ожидал {token_type!r}")

class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type
    def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
    ):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)



async def get_current_auth_user_refresh(
    payload: dict = Depends(get_current_token_payload),
) -> SUsers:
    validate_token_type(payload,REFRESH_TOKEN_TYPE)
    return await get_user_by_token_sub(payload)


def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload)
        )-> SUsers:
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload)
    return get_auth_user_from_token


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)


def get_current_active_auth_user(
    user: SUsers = Depends(get_current_auth_user)
 ):   
    if user.is_active:
        return user
    raise UserInActive 





