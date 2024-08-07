from app.DAO.base import BaseDAO
from app.users.models import Users
from app.users.sms_codes.models import SmsCodes
from app.database import async_session_maker
from sqlalchemy import desc, select

class SmsCodesDAO(BaseDAO):
    model = SmsCodes



    @classmethod
    async def last_sms_code(cls, user_id):
        async with async_session_maker() as session:
            query = (
            select(SmsCodes)
            .join(Users, SmsCodes.user_id == Users.id)
            .where(Users.id == user_id, SmsCodes.is_used == False)
            .order_by(desc(SmsCodes.id))
            .limit(1)
            )
            result = await session.execute(query)
            latest_smscode = result.scalar_one_or_none()
            return latest_smscode