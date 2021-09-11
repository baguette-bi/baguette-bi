from typing import Optional

from baguette_bi.core.connections.query_builders.sql.standard import (
    StandardSQLQueryBuilder,
)
from baguette_bi.core.connections.sql_alchemy import SQLAlchemyConnection


class PostgresQueryBuilder(StandardSQLQueryBuilder):
    pass


class PostgresConnection(SQLAlchemyConnection):
    """User-facing Postgres connection supporting SQL transforms."""

    query_builder = PostgresQueryBuilder()

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
