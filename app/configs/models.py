from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import SettingsConfigDict

from app.configs.base import EnvSettings

class ModelsSettings(EnvSettings):
    model_config = SettingsConfigDict(env_prefix="MODELS_")
    
    embedding_model: str = ''
    llm_model: str = ''


@lru_cache
def get_models_settings():
    return ModelsSettings()

ModelsSettingsDep = Annotated[ModelsSettings, Depends(get_models_settings)]
