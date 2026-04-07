from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    database_url: str
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env", extra="ignore")




settings = Settings()