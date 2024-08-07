from pydantic import BaseModel, EmailStr

class SUsers(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: int
    email: EmailStr
    hashed_password: str
    type_user_id: int
    is_active: bool
    is_confirmed: bool
    registration_attempts: int
    discount: int

