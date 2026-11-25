from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import SettingsConfigDict

from app.configs.base import EnvSettings

class FaqSettings(EnvSettings):
    model_config = SettingsConfigDict(env_prefix="FAQ_")
    
    min_confidence: float = 0.5


@lru_cache
def get_faq_settings():
    return FaqSettings()

FaqSettingsDep = Annotated[FaqSettings, Depends(get_faq_settings)]
