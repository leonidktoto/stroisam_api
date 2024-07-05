from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# DB_HOST = '127.0.0.1'
# DB_PORT =
# DB_USER =
# DB_PASS =
# DB_NAME =

# DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME }"


async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,  # В консоль будут выводиться все запросы в консоль
    #   pool_size=5, # Количество подключений
    #   max_overflow=10, # Дополнительные подключения, если основные заполнены
)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
