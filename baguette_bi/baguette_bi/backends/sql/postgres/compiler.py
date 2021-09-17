from baguette_bi.backends.sql.base.compiler import SQLCompiler, SQLFunctionCompiler
from baguette_bi.backends.sql.base.functions import (
    CastSQLFunction,
    ClampSQLFunction,
    ExtractSQLFunction,
    PadSQLFunction,
    SQLFunction,
    SubstrSQLFunction,
    TruncateSQLFunction,
)


class PostgresFunctionCompiler(SQLFunctionCompiler):
    toBoolean = CastSQLFunction("bool")
    toDate = CastSQLFunction("date")
    toNumber = CastSQLFunction("float")
    toString = CastSQLFunction("varchar")
    if_ = SQLFunction(name="if", nargs={2, 3})
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
    max = SQLFunction("greatest")
    min = SQLFunction("least")
    pow = SQLFunction("power")
    random = SQLFunction()
    round = SQLFunction(nargs={1, 2})
    sin = SQLFunction()
    sqrt = SQLFunction()
    tan = SQLFunction()
    now = SQLFunction()

    date = ExtractSQLFunction("day")
    day = ExtractSQLFunction("dow")
    dayofyear = ExtractSQLFunction("doy")
    year = ExtractSQLFunction("year")
    quarter = ExtractSQLFunction("quarter")
    month = ExtractSQLFunction("month")
    week = ExtractSQLFunction("week")
    hour = ExtractSQLFunction("hour")
    minutes = ExtractSQLFunction("minute")
    seconds = ExtractSQLFunction("second")
    milliseconds = ExtractSQLFunction("millisecond")
    time = ExtractSQLFunction("epoch")
    length = SQLFunction()
    lower = SQLFunction()
    pad = PadSQLFunction()
    parseFloat = CastSQLFunction("float")
    parseInt = CastSQLFunction("int")
    replace = SQLFunction(name="replace", nargs=3)
    slice = SubstrSQLFunction()
    substring = SubstrSQLFunction()
    trim = SQLFunction()
    truncate = TruncateSQLFunction()
    upper = SQLFunction()


class PostgresCompiler(SQLCompiler):
    function_compiler = PostgresFunctionCompiler()
