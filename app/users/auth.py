from datetime import datetime, timezone
from typing import Optional
from app.users.dao import UsersDAO
from app.exceptions import SmsValidationExpired, UserIsNotRegisteredException, IncorrectSmsValidationException
from app.users.models import Users
from app.users.sms_codes.dao import SmsCodesDAO
from app.users.sms_codes.models import SmsCodes



async def send_sms(id: int, sms:str):
    pass




