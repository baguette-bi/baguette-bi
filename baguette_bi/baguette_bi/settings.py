from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseSettings

from baguette_bi.examples import docs


class Settings(BaseSettings):
    project: str = str(Path(docs.__file__).parent)
    pages_dir: str = "pages"

    web_host: str = "127.0.0.1"
    web_port: int = 8000
    web_daemon: bool = False
    web_workers: int = 1
    web_max_requests: int = 0

    auth: bool = False
    session_max_age: int = 3600 * 24  # 24 hours
    secret_key: str = "secret"
    database_url: str = "sqlite:///baguette.db"
    default_admin_password: str = "baguette"

    cache: Literal["none", "redis"] = "none"
    cache_ttl: int = 60 * 20  # 20 minutes
    redis_host: str = "localhost"  # Disabled by default
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None

    icon: str = "🥖"
    title: str = "Baguette BI"
    locale: str = "en_US.UTF-8"

    debug: bool = False

    class Config:
        env_file = ".env"
        env_prefix = "baguette_"


settings = Settings()
