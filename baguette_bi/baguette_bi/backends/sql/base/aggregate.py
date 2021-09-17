from baguette_bi.backends.sql.base.compiler import SQLFunctionCompiler
from baguette_bi.backends.sql.base.functions import (
    NotImplementedSQLFunction,
    SQLFunction,
)


class AggregateFunctionCompiler(SQLFunctionCompiler):
    count = staticmethod(lambda x: "count(*)")
    valid = staticmethod(lambda x: f'count(case when "{x}" is not null then 1 end)')
    missing = staticmethod(lambda x: f'count(case when "{x}" is null then 1 end)')
    distinct = staticmethod(lambda x: f'count(distinct "{x}")')
    sum = SQLFunction()
    mean = SQLFunction("avg")
    average = SQLFunction("avg")
    variance = SQLFunction("var_samp")
    variancep = SQLFunction("var_pop")
    stdev = SQLFunction("stddev_samp")
    stdevp = SQLFunction("stddev_pop")
    stderr = NotImplementedSQLFunction()  # TODO: probably can compute in SQL

    # TODO: can't calculate as an aggregate, maybe install some extensions?
    median = NotImplementedSQLFunction()

    min = SQLFunction()
    max = SQLFunction()

    q1 = NotImplementedSQLFunction()
    q3 = NotImplementedSQLFunction()
    ci0 = NotImplementedSQLFunction()
    ci1 = NotImplementedSQLFunction()

    # TODO: need some way to do multi-step aggregates for median, this etc.
    argmin = NotImplementedSQLFunction()
    argmax = NotImplementedSQLFunction()
