from baguette_bi.connections.query_builders.sql.standard import StandardSQLQueryBuilder
from baguette_bi.connections.sql_alchemy import SQLAlchemyConnection


class SQLiteQueryBuilder(StandardSQLQueryBuilder):
    pass


class SQLiteConnection(SQLAlchemyConnection):
    query_builder = SQLiteQueryBuilder()

    def __init__(self, file: str):
        super().__init__(driver="sqlite", database=file)
