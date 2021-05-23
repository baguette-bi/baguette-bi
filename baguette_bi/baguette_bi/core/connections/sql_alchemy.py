import pandas as pd
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL

from baguette_bi.core.data_request import DataRequest

from .base import Connection


class SQLAlchemyConnection(Connection):
    type: str = "sql_alchemy"

    def __init__(
        self,
        driver="sqlite",
        username=None,
        password=None,
        host=None,
        port=None,
        database=None,
    ):
        super().__init__(
            drivername=driver,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
        )
        self._engine = None
        self.url = URL(**self.details)

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_engine(self.url)
        return self._engine

    def execute(self, req: DataRequest) -> pd.DataFrame:
        return pd.read_sql(req.query, self.engine)
