from baguette_bi.backends.sql.base.query import SQLQuery
from baguette_bi.backends.sql.sqlite.compiler import SQLiteCompiler


class SQLiteQuery(SQLQuery):
    compiler = SQLiteCompiler()
