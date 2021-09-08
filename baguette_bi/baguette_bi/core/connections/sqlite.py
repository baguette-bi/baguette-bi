from baguette_bi.core.connections.sql_alchemy import SQLAlchemyConnection
from baguette_bi.core.connections.transforms.sql.sqlite import SQLiteSQLTransformMixin


class SQLiteConnection(SQLAlchemyConnection, SQLiteSQLTransformMixin):
    def __init__(self, file: str):
        super().__init__(driver="sqlite", database=file)
