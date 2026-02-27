from pathlib import Path
from tempfile import gettempdir

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RESOURCES_PATH: Path = Path(__file__).resolve().parent.parent / "resources"
    TRANSLATION_PATH: Path = Path(gettempdir()).resolve() / "postdb"

    ALLOWED_ORIGINS: list[str] = Field(...)
    ALLOWED_METHODS: list[str] = Field(...)
    ALLOWED_HEADERS: list[str] = Field(...)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
