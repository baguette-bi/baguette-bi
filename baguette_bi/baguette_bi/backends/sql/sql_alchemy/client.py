from typing import Optional

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from baguette_bi.backends.base.client import Client


class SQLAlchemyClient(Client):
    """We're using SQL Alchemy for connections when it's possible, because it handles
    connection pooling automatically
    """

    def __init__(
        self,
        driver: str = "sqlite",
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
    ):
        self._engine = None
        self.url = URL.create(
            drivername=driver,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
        )

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_engine(self.url)
        return self._engine

    def execute(self, query, parameters) -> pd.DataFrame:
        return pd.read_sql(query, self.engine, params=parameters).fillna(np.nan)

    def details(self) -> dict:
        return {"url": str(self.url)}
