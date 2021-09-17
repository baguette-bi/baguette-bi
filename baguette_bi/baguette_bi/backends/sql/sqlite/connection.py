from baguette_bi.backends.base.connection import Connection
from baguette_bi.backends.sql.sqlite.client import SQLiteClient
from baguette_bi.backends.sql.sqlite.query import SQLiteQuery


class SQLiteConnection(Connection):
    type = "sqlite"
    query_cls = SQLiteQuery

    def __init__(self, database: str):
        client = SQLiteClient(database=database)
        super().__init__(client)
