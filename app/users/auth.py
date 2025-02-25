from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.AUTHJWT.private_key_path.read_text(),
    algorithm: str = settings.AUTHJWT.algorithm,
    expire_minutes: int = settings.AUTHJWT.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
    admin_access_expire_minuts: int = settings.AUTHJWT.admin_access_token_expire_minuts,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    if payload.get("type") == "access" and payload.get("role") == 2:
        expire = now + timedelta(minutes=admin_access_expire_minuts)

    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.AUTHJWT.public_key_path.read_text(),
    algorithm: str = settings.AUTHJWT.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_passsword(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
