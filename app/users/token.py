from fastapi import Response
from app.users.schemas import SUsers
from app.config import settings
from app.users import auth
from datetime import timedelta

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def create_jwt(
    token_type: str, 
    token_data: dict, 
    expire_minutes: int = settings.AUTHJWT.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
    ) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD : token_type}
    jwt_payload.update(token_data)
    return auth.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta
        )


def create_access_token(user: SUsers) -> str:
    jwt_payload = {
        "sub": user.phone,
        "username": user.phone,
        "email" : user.email,
        "role" : user.type_user_id
    }
    return create_jwt(
        token_type = ACCESS_TOKEN_TYPE, 
        token_data = jwt_payload,
        expire_minutes = settings.AUTHJWT.access_token_expire_minutes
        )

def create_refresh_token(user: SUsers) -> str:
    jwt_payload = {
        "sub": user.phone,
        #"username": user.phone,
    }
    return create_jwt(
        token_type = REFRESH_TOKEN_TYPE, 
        token_data = jwt_payload, 
        expire_timedelta = timedelta(days=settings.AUTHJWT.refresh_token_expire_days)
        )

def auth_user_set_cookie(response: Response, token_type: str, token: str):

    max_age = 0
    if token_type == ACCESS_TOKEN_TYPE:
        max_age = settings.AUTHJWT.access_token_expire_minutes*60
    if token_type == REFRESH_TOKEN_TYPE:
        max_age = settings.AUTHJWT.access_token_expire_minutes*1440*60

    response.set_cookie(
        token_type, 
        token, 
        httponly = True, 
        max_age = max_age
    )

