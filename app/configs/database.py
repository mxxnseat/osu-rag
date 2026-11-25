from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:1234@localhost:5432/osu"

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings() -> DatabaseSettings:
    return DatabaseSettings()

DatabaseSettingsDep = Annotated[DatabaseSettings, Depends(get_settings)]