from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"
ROOT_DIR = Path(__file__).resolve().parents[3]
DEFAULT_SQLITE_PATH = ROOT_DIR / "backend" / "data" / "finflow.db"


class Settings(BaseSettings):
    app_name: str = "FinFlow"
    api_prefix: str = "/api"
    database_url: str = f"sqlite+aiosqlite:///{DEFAULT_SQLITE_PATH.as_posix()}"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 43200
    youtube_api_key: str = ""
    bilibili_sessdata: str = ""
    nginx_conf_file: str = "nginx.http.conf"

    model_config = SettingsConfigDict(
        env_file=str(ROOT_ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
