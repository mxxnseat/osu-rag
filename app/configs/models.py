from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict

class ModelsSettings(BaseSettings):
    embedding_model: str = ''

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_models_settings():
    return ModelsSettings()

ModelsSettingsDep = Annotated[ModelsSettings, Depends(get_models_settings)]
