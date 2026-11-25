from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from pydantic_settings import SettingsConfigDict

from app.configs.base import EnvSettings

class DatabaseSettings(EnvSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")
    
    url: str = "postgresql+psycopg://postgres:1234@localhost:5432/osu"

@lru_cache
def get_settings() -> DatabaseSettings:
    return DatabaseSettings()

DatabaseSettingsDep = Annotated[DatabaseSettings, Depends(get_settings)]