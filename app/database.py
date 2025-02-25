from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# DB_HOST = '127.0.0.1'
# DB_PORT =
# DB_USER =
# DB_PASS =
# DB_NAME =

# DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME }"

if settings.MODE == "TEST":
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_PARAMS = {}


sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,  # В консоль будут выводиться все запросы в консоль
    #   pool_size=5, # Количество подключений
    #   max_overflow=10, # Дополнительные подключени, если основные заполнены
    **DATABASE_PARAMS
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,  # В консоль будут выводиться все запросы в консоль
    #   pool_size=5, # Количество подключений
    #   max_overflow=10, # Дополнительные подключения, если основные заполнены
    **DATABASE_PARAMS
)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
sync_session = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass
