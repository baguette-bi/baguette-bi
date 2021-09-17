from typing import Optional

from baguette_bi.backends.sql.base.connection import SQLConnection
from baguette_bi.backends.sql.postgres.client import PostgresClient


class PostgresConnection(SQLConnection):
    type = "postgres"

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "postgres",
        username: str = "postgres",
        password: Optional[str] = None,
    ):
        client = PostgresClient(
            host=host,
            port=port,
            database=database,
            username=username,
            password=password,
        )
        super().__init__(client)
