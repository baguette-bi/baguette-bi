from pathlib import Path

from pydantic import BaseSettings

from baguette_bi.core.permissions import Permissions
from baguette_bi.examples import altair_examples


class Settings(BaseSettings):
    project: str = str(Path(altair_examples.__file__).parent.resolve())
    secret_key: str = "secret"

    auth: bool = False
    root_permissions: Permissions = Permissions.authenticated
    database_url: str = "sqlite:///baguette.db"
    default_admin_password: str = "baguette"

    session_max_age: int = 3600 * 24  # 24 hours

    icon: str = "🥖"
    title: str = "Baguette BI"

    class Config:
        env_file = ".env"
        env_prefix = "baguette_"


settings = Settings()
