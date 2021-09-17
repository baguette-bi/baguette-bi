from typing import Optional

from baguette_bi.backends.sql.sql_alchemy.client import SQLAlchemyClient


class PostgresClient(SQLAlchemyClient):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "postgres",
        username: str = "postgres",
        password: Optional[str] = None,
    ):
        super().__init__(
            driver="postgresql",
            host=host,
            port=port,
            database=database,
            username=username,
            password=password,
        )
