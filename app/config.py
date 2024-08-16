from typing import Literal
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR=Path(__file__).parent.parent

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR/ "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR/ "certs" / "jwt-public.pem"
    algorithm: str = "RS256" 
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

print(BASE_DIR)

class Settings_env(BaseSettings):

    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO"]
    
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITM: str
    AUTHJWT: AuthJWT = AuthJWT()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self): #Синхронное подключение формируем dsn
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings_env()  # type: ignore
# print(settings.DATABASE_URL)
