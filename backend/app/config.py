from urllib.parse import quote
from pydantic import HttpUrl, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    url: HttpUrl
    postgres_password: str = "gis_secure_password"
    postgres_user: str = "gis_user"
    postgres_db: str = "parcel_db"
    db_host: str = "db"
    db_port: int = 5432

    @computed_field
    @property
    def postgres_dsn(self) -> PostgresDsn:
        user = quote(self.postgres_user)
        password = quote(self.postgres_password)

        return PostgresDsn(
            f"postgresql://{user}:{password}@{self.db_host}:{self.db_port}/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
