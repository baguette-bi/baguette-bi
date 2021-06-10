from pathlib import Path

from pydantic import BaseSettings

from baguette_bi.examples import docs


class Settings(BaseSettings):
    project: str = str(Path(docs.__file__).parent)
    pages_dir: str = "pages"

    auth: bool = False
    session_max_age: int = 3600 * 24  # 24 hours
    secret_key: str = "secret"
    database_url: str = "sqlite:///baguette.db"
    default_admin_password: str = "baguette"

    icon: str = "🥖"
    title: str = "Baguette BI"
    locale: str = "en_US.UTF-8"

    debug: bool = True

    class Config:
        env_file = ".env"
        env_prefix = "baguette_"


settings = Settings()
