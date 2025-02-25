from celery import Task
from smsaero import SmsAero, SmsAeroException

from app.config import settings
from app.tasks.celery import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_sms_message(self: Task, user_phone: int, message: str):
    try:
        # Создаем экземпляр API
        api = SmsAero(settings.SMSAERO_EMAIL, settings.SMSAERO_API_KEY)
        # Отправляем SMS
        response = api.send_sms(user_phone, message)
        return response
    except SmsAeroException as e:
        # Повторная попытка
        raise self.retry(exc=e)
