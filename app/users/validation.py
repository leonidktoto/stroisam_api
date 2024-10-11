
from datetime import datetime, timezone
from typing import Optional
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from app.exceptions import IncorrectSmsValidationException, IncorrectTokenFormatException, InvalidToken, InvalidTokenType, SmsValidationExpired, TokenAbsentException, UserInActive, UserIsNotRegisteredException, UserNotAdmin
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
    await UsersDAO.update_data({"registration_attempts": 0}, id=user.id)

    return user

# Изменяем функцию для получения токена из куки по типу токена (access или refresh)
def get_token_from_request_by_type(request: Request, token_type: str) -> Optional[str]:
    if token_type == ACCESS_TOKEN_TYPE:
        return request.cookies.get(ACCESS_TOKEN_TYPE)
    elif token_type == REFRESH_TOKEN_TYPE:
        return request.cookies.get(REFRESH_TOKEN_TYPE)
    return None

# Получаем payload из токена в зависимости от типа
def get_current_token_payload(request: Request, token_type: str) -> dict:
    token = get_token_from_request_by_type(request, token_type)
    if not token:
        raise TokenAbsentException
    try:
        payload = auth.decode_jwt(token)
    except InvalidTokenError:
        raise IncorrectTokenFormatException
    return payload

# Асинхронная функция для получения пользователя по sub из payload
async def get_user_by_token_sub(payload: dict) -> SUserAuth:
    username: str | None = payload.get("sub")
    user: Optional[Users] = await UsersDAO.find_one_or_none(phone=username)
    if not user:
        raise UserIsNotRegisteredException
    return user

# Валидация типа токена
def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise InvalidToken(detail=f"Неверный тип токена {current_token_type!r}, ожидался {token_type!r}")

# Фабричная функция для получения авторизованного пользователя по типу токена
def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(
       # request: Request,  # Получаем объект Request напрямую
        payload: dict = Depends(get_current_token_payload_with_type(token_type))  # Зависимость для токена
    ) -> SUsers:
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload)
    return get_auth_user_from_token

# Вспомогательная функция для передачи token_type через Depends
def get_current_token_payload_with_type(token_type: str):
    def _get_current_token_payload(request: Request):
        return get_current_token_payload(request, token_type)
    return _get_current_token_payload

# Динамическое создание зависимостей для access и refresh токенов
get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)

# Функция для получения текущего активного пользователя
def get_current_active_auth_user(
    user: SUsers = Depends(get_current_auth_user)
):
    if user.is_active:
        return user
    raise UserInActive

# Функция для проверки роли администратора
def get_admin_active_auth_user(
    user: SUsers = Depends(get_current_active_auth_user)
):
    if user.type_user_id == 2:
        return user
    raise UserNotAdmin