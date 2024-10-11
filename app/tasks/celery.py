from celery import Celery
from app.config import settings


# Ваша текущая конфигурация Celery
celery_app = Celery('tasks')

celery_app.conf.update(
    broker_url=settings.REDIS_URL,
    result_backend=settings.REDIS_URL,
    # Добавьте это для версий Celery 6.0 и выше
    broker_connection_retry_on_startup=True,  # Повторные попытки подключения на старте
    result_expires=3600,  # Результаты хранятся 1 час
    include=["app.tasks.tasks"],
)


