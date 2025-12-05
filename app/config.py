from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    jwt_secret: str
    supabase_url: str
    supabase_key: str
    database_name: str
    allowed_origins: List[str] = ["*"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
