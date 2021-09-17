from baguette_bi.backends.sql.sql_alchemy.client import SQLAlchemyClient


class SQLiteClient(SQLAlchemyClient):
    def __init__(self, database: str):
        super().__init__(driver="sqlite", database=database)
