from pydantic import BaseModel, EmailStr, Field

class SUsers(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: int
    email: EmailStr
    hashed_password: str | None
    type_user_id: int
    is_active: bool
    is_confirmed: bool
    registration_attempts: int
    discount: int


class SUserAuth(SUsers):
    hashed_password: str | None = Field(exclude=True)
    is_active: bool = Field(exclude=True)
    is_confirmed: bool = Field(exclude=True)
    registration_attempts: int = Field(exclude=True)

class SRegisterUser(BaseModel):
    first_name: int
    last_name: int | None
    phone: int
    email: EmailStr

class STokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"