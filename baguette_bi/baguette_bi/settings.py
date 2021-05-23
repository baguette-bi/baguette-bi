from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseSettings

from .examples import altair_examples


class Settings(BaseSettings):
    project: str = str(Path(altair_examples.__file__).parent.resolve())
    secret_key: str = "secret"
    executor: Literal["local", "celery"] = "local"

    database_url: Optional[str] = None
    celery_broker_url: Optional[str] = None

    icon: str = "🥖"
    title: str = "Baguette BI"

    class Config:
        env_prefix = "baguette_"


settings = Settings()
