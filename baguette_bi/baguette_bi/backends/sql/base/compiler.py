import math

from baguette_bi.backends.base.compiler import Compiler
from baguette_bi.backends.sql.base.functions import NotImplementedSQLFunction


def binop(op):
    """Generate a method for generating a binary infix operation from 2 arguments."""
    return staticmethod(lambda x: f"{x[0]} {op} {x[1]}")


def raise_expression_incompatible(expr):
    @staticmethod
    def raise_():
        raise ValueError(
            f"Vega expression {expr} is meaningless in SQL and isn't supported"
        )

    return raise_


class SQLFunctionCompiler:
    """Each method, when called, will return a rendered function call. To avoid breaking
    changed, implementation should be done for each dialect separately. Some standard
    functions are provided in the functions module.
    """

    def __getattr__(self, name: str):
        return NotImplementedSQLFunction()

    toBoolean = NotImplementedSQLFunction()
    toDate = NotImplementedSQLFunction()
    toNumber = NotImplementedSQLFunction()
    toString = NotImplementedSQLFunction()
    if_ = NotImplementedSQLFunction()
    abs = NotImplementedSQLFunction()
    acos = NotImplementedSQLFunction()
    asin = NotImplementedSQLFunction()
    atan = NotImplementedSQLFunction()
    atan2 = NotImplementedSQLFunction()
    ceil = NotImplementedSQLFunction()
    clamp = NotImplementedSQLFunction()
    cos = NotImplementedSQLFunction()
    exp = NotImplementedSQLFunction()
    floor = NotImplementedSQLFunction()
    log = NotImplementedSQLFunction()
    max = NotImplementedSQLFunction()
    min = NotImplementedSQLFunction()
    pow = NotImplementedSQLFunction()
    random = NotImplementedSQLFunction()
    round = NotImplementedSQLFunction()
    sin = NotImplementedSQLFunction()
    sqrt = NotImplementedSQLFunction()
    tan = NotImplementedSQLFunction()
    now = NotImplementedSQLFunction()

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
    length = NotImplementedSQLFunction()
    lower = NotImplementedSQLFunction()
    pad = NotImplementedSQLFunction()
    parseFloat = NotImplementedSQLFunction()
    parseInt = NotImplementedSQLFunction()
    replace = NotImplementedSQLFunction()
    slice = NotImplementedSQLFunction()
    substring = NotImplementedSQLFunction()
    trim = NotImplementedSQLFunction()
    truncate = NotImplementedSQLFunction()
    upper = NotImplementedSQLFunction()


class SQLCompiler(Compiler):
    """Compiles Vega Expressions AST to SQL str.

    Should support most SQL dialects, which differ only in function sets, so functions
    are implemented as a separate compiler.
    """

    function_compiler = SQLFunctionCompiler()

    def _quote_identifier(self, token):
        return f'"{token}"'

    def _quote_string(self, token):
        return f"'{token}'"

    # CONSTANTS

    NAN = raise_expression_incompatible("NaN")

    def NULL(self, token):
        return "null"

    UNDEFINED = raise_expression_incompatible("undefined")

    def E(self, token):
        return math.e

    def LN2(self, token):
        return math.log(2)

    def LN10(self, token):
        return math.log(10)

    def LOG2E(self, token):
        return math.log2(math.e)

    def LOG10E(self, token):
        return math.log10(math.e)

    MAX_VALUE = raise_expression_incompatible("MAX_VALUE")
    MIN_VALUE = raise_expression_incompatible("MIN_VALUE")

    def PI(self, token):
        return math.pi

    def SQRT1_2(self, token):
        return math.sqrt(0.5)

    def SQRT2(sel, token):
        return math.sqrt(2)

    # LITERALS

    def TRUE(self, token):
        return "true"

    def FALSE(self, token):
        return "false"

    INTEGER = int
    NUMBER = float
    STRING = str

    def FIELD(self, token):
        return self._quote_identifier(token)

    # OPERATIONS

    def paren(self, token):
        return f"({token[0]})"

    def not_(self, token):
        return f"not {token}"

    def neg(self, token):
        return f"-{token[0]}"

    # BINARY

    pow = binop("^")
    mul = binop("*")
    div = binop("/")
    mod = binop("%")
    add = binop("+")
    sub = binop("-")
    gt = binop(">")
    gte = binop(">=")
    lt = binop("<")
    lte = binop("<=")
    eq = binop("=")
    ne = binop("<>")
    and_ = binop("and")
    or_ = binop("or")
    concat = binop("||")

    def tern(self, token):  # ternary
        a, b, c = token
        return f"case when {a} then {b} else {c} end"

    def call(self, token):
        fn, *args = token
        fn = "if_" if fn == "if" else fn
        fn = getattr(self.function_compiler, fn)
        return fn(args)

    def expr(self, token):  # root expr
        return token[0]
