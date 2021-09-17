from baguette_bi.backends.sql.base.query import SQLQuery
from baguette_bi.backends.sql.postgres.compiler import PostgresCompiler


class PostgresQuery(SQLQuery):
    compiler = PostgresCompiler()
