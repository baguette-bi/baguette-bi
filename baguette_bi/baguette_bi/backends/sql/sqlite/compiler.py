from baguette_bi.backends.sql.base.compiler import SQLCompiler, SQLFunctionCompiler
from baguette_bi.backends.sql.base.functions import (
    CastSQLFunction,
    ClampSQLFunction,
    NotImplementedSQLFunction,
    PadSQLFunction,
    SQLFunction,
    SubstrSQLFunction,
    TernarySQLFunction,
    TruncateSQLFunction,
)


class SQLiteFunctionCompiler(SQLFunctionCompiler):
    toNumber = CastSQLFunction("real")
    toString = CastSQLFunction("text")
    if_ = TernarySQLFunction()
    abs = SQLFunction()
    acos = SQLFunction()
    asin = SQLFunction()
    atan = SQLFunction()
    atan2 = SQLFunction()
    ceil = SQLFunction()
    clamp = ClampSQLFunction()
    cos = SQLFunction()
    exp = SQLFunction()
    floor = SQLFunction()
    log = SQLFunction("ln")
    max = SQLFunction()
    min = SQLFunction()
    pow = SQLFunction("power")
    random = SQLFunction()
    round = SQLFunction(nargs={1, 2})
    sin = SQLFunction()
    sqrt = SQLFunction()
    tan = SQLFunction()

    date = NotImplementedSQLFunction()
    day = NotImplementedSQLFunction()
    dayofyear = NotImplementedSQLFunction()
    year = NotImplementedSQLFunction()
    quarter = NotImplementedSQLFunction()
    month = NotImplementedSQLFunction()
    week = NotImplementedSQLFunction()
    hour = NotImplementedSQLFunction()
    minutes = NotImplementedSQLFunction()
    seconds = NotImplementedSQLFunction()
    milliseconds = NotImplementedSQLFunction()
    time = NotImplementedSQLFunction()

    length = SQLFunction()
    lower = SQLFunction()
    pad = PadSQLFunction()
    parseFloat = CastSQLFunction("real")
    parseInt = CastSQLFunction("real")
    replace = SQLFunction()
    slice = SubstrSQLFunction()
    substring = SubstrSQLFunction()
    trim = SQLFunction()
    truncate = TruncateSQLFunction()
    upper = SQLFunction()


class SQLiteCompiler(SQLCompiler):
    function_compiler = SQLiteFunctionCompiler()
