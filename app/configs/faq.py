from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict

class FaqSettings(BaseSettings):
    embedding_model: str = ''

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_faq_settings():
    return FaqSettings()

FaqSettingsDep = Annotated[get_faq_settings, Depends(get_faq_settings)]
