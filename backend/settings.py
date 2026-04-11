from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    admin_token: str
    enable_polling: bool = True

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env", extra="ignore"
    )


settings = Settings()
