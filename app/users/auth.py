from datetime import timedelta, datetime, timezone
import bcrypt
from os import read
import jwt
from app.config import AuthJWT, settings



def encode_jwt(
    payload: dict,
    private_key: str = settings.AUTHJWT.private_key_path.read_text(),
    algorithm: str = settings.AUTHJWT.algorithm,
    expire_minutes: int =settings.AUTHJWT.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    print(payload)
    if payload["type"] == "access" and payload["role"] == 1:
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
    else: 
        expire = now + timedelta(minutes=120)
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.AUTHJWT.public_key_path.read_text(),
    algorithm: str = settings.AUTHJWT.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm]
    )
    return decoded


def hash_passsword(
    password: str
) -> bytes:
     salt=bcrypt.gensalt()
     pwd_bytes: bytes = password.encode()
     return bcrypt.hashpw(pwd_bytes, salt)

def validate_password(
    password: str, 
    hashed_password: bytes 
    ) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


