from baguette_bi.core.connections.sql_alchemy import SQLAlchemyConnection
from baguette_bi.core.connections.transforms.sql.postgres import (
    PostgresSQLTransformMixin,
)


class PostgresConnection(SQLAlchemyConnection, PostgresSQLTransformMixin):
    """User-facing Postgres connection supporting SQL transforms."""
