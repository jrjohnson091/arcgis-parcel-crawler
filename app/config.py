from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    url: HttpUrl

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()