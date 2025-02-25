import random

from app.tasks.tasks import send_sms_message
from app.users.dao import UsersDAO
from app.users.schemas import SUsers
from app.users.sms_codes.dao import SmsCodesDAO


def generate_sms_code():
    return str(random.randint(100000, 999999))


async def send_new_sms_code(user: SUsers, phone: str):
    code = generate_sms_code()
    # hash_code=hash_passsword(code) включить хэширование пароля
    await SmsCodesDAO.add_data(user_id=user.id, code=code)
    await UsersDAO.update_data(
        {"registration_attempts": user.registration_attempts + 1}, id=user.id
    )
    send_sms_message.delay(int(f"7{phone}"), code)  # type: ignore
    return {"status": "ok"}
