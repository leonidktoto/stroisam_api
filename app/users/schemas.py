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
    first_name: str = Field(..., max_length=15)
    email: EmailStr
    phone: str = Field(
        ..., pattern=r"^\d{10}$", description="Номер телефона (ровно 10 цифр)", title="Строка"
    )
    last_name: str | None = Field(None, max_length=15)


class STokenInfo(BaseModel):
    access: str
    refresh: str | None = None
    # token_type: str = "Bearer"


class SUsersPhone(BaseModel):
    phone: str = Field(
        ..., pattern=r"^\d{10}$", description="Номер телефона (ровно 10 цифр)", title="Строка"
    )
