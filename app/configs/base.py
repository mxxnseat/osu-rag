from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvSettings(BaseSettings):
    __hash__ = object.__hash__

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
