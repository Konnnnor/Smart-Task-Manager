import os

from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHMS: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*7
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SYNC_DATABASE_URL: str = os.getenv("SYNC_DATABASE_URL")

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

        