import os

from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*7
    DATABASE_URL: str
    SYNC_DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore",env_file_encoding="utf-8")

settings = Settings()

        