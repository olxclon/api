from functools import lru_cache
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str
    supabase_url: str
    supabase_key: str
    database_name: str
    allowed_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
