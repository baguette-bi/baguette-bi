from baguette_bi.connections.query_builders.base import BaseQueryBuilder
from baguette_bi.connections.query_builders.sql.utils import NotImplementedSQLFunction


class BaseSQLQueryBuilder(BaseQueryBuilder):
    count = NotImplementedSQLFunction()
    valid = NotImplementedSQLFunction()
    values = NotImplementedSQLFunction()
    missing = NotImplementedSQLFunction()
    distinct = NotImplementedSQLFunction()
    sum = NotImplementedSQLFunction()
    product = NotImplementedSQLFunction()
    mean = NotImplementedSQLFunction()
    average = NotImplementedSQLFunction()
    variance = NotImplementedSQLFunction()
    variancep = NotImplementedSQLFunction()
    stdev = NotImplementedSQLFunction()
    stdevp = NotImplementedSQLFunction()
    stderr = NotImplementedSQLFunction()
    median = NotImplementedSQLFunction()
    min = NotImplementedSQLFunction()
    max = NotImplementedSQLFunction()
    q1 = NotImplementedSQLFunction()
    q3 = NotImplementedSQLFunction()
    ci0 = NotImplementedSQLFunction()
    ci1 = NotImplementedSQLFunction()
    argmin = NotImplementedSQLFunction()
    argmax = NotImplementedSQLFunction()
