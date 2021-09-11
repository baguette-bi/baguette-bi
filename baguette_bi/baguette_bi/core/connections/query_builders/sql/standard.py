import math

import altair as alt
from jinja2 import Template
from lark import Transformer

from baguette_bi.altair.expr import parser
from baguette_bi.core.connections.query_builders.sql.base import BaseSQLQueryBuilder
from baguette_bi.core.connections.query_builders.sql.errors import (
    SQLExpressionCompilationError,
    SQLFunctionCompilationError,
)
from baguette_bi.core.connections.query_builders.sql.utils import (
    NotImplementedSQLFunction,
    just_fn,
)

groupby_query_template = Template(
    """
select {{ ", ".join(select_list) }}
from ({{ source }}) as t
{% if groupby_list %}
group by {{ ", ".join(groupby_list) }}
{% endif %}
"""
)

joinaggregate_query_template = Template(
    """
select *, {{ ", ".join(select_list) }}
from ({{ source }}) as t
"""
)


def binop(op):
    return staticmethod(lambda x: f"{x[0]} {op} {x[1]}")


def just_call(fn):
    return staticmethod(lambda args: f"fn({', '.join(args)})")


class StandardSQLVegaExpressionTransformer(Transformer):

    # CONSTANTS

    def NAN(self, token):
        raise SQLExpressionCompilationError("NaN")

    def NULL(self, token):
        return "null"

    def UNDEFINED(self, token):
        raise SQLExpressionCompilationError("undefined")

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

    def MAX_VALUE(self, token):
        raise SQLExpressionCompilationError("MAX_VALUE")

    def MIN_VALUE(self, token):
        raise SQLExpressionCompilationError("MIN_VALUE")

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

    def INTEGER(self, token):
        return token

    def NUMBER(self, token):
        return token

    def STRING(self, token):
        return token

    def FIELD(self, token):
        return token

    # OPERATIONS

    def paren(self, token):
        return f"({token[0]})"

    def not_(self, token):
        return f"not {token}"

    def neg(self, token):
        return f"-{token}"

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

    def tern(self, token):  # ternary
        a, b, c = token
        return f"case when {a} then {b} else {c} end"

    def call(self, token):
        fn, *args = token
        fn = "if_" if fn == "if" else fn
        if not hasattr(self, fn):
            raise SQLFunctionCompilationError(fn)
        fn = getattr(self, fn)
        return fn(args)

    def expr(self, token):  # root expr
        return token[0]

    # FUNCTIONS

    def if_(self, args):
        return self.tern(args)

    # isNaN
    # isFinite

    abs = just_call("abs")
    acos = just_call("acos")
    asin = just_call("asin")
    atan = just_call("atan")
    atan2 = just_call("atan2")
    ceil = just_call("ceil")

    def clamp(self, args):
        val, mi, ma = args
        return (
            f"case when {val} < {mi} then {mi} "
            f"when {val} > {ma} then {ma} else {val} end"
        )

    cos = just_call("cos")
    exp = just_call("exp")
    floor = just_call("floor")
    log = just_call("log")
    min = just_call("least")
    max = just_call("greatest")
    pow = just_call("pow")
    random = just_call("random")
    round = just_call("round")
    sin = just_call("sin")
    sqrt = just_call("sqrt")
    tan = just_call("tan")

    now = just_call("sysdate")

    # date


transformer = StandardSQLVegaExpressionTransformer()


class StandardSQLQueryBuilder(BaseSQLQueryBuilder):
    """An implementation that aims to be closest the "standard" SQL (whatever that is,
    the standard itself is not open) and require minimal amount of tweaking to create
    builders for other SQL dialects. In practice, this is close to e.g. SQLite, Postgres
    and Vertica dialects.
    """

    count = staticmethod(lambda x: "count(*)")
    valid = staticmethod(lambda x: f'count(case when "{x}" is not null then 1 end)')
    values = just_fn("array_agg")
    missing = staticmethod(lambda x: f'count(case when "{x}" is null then 1 end)')
    distinct = staticmethod(lambda x: f'count(distinct "{x}")')
    sum = just_fn("sum")
    product = NotImplementedSQLFunction()
    mean = just_fn("avg")
    average = just_fn("avg")
    variance = just_fn("var_samp")
    variancep = just_fn("var_pop")
    stdev = just_fn("stddev_samp")
    stdevp = just_fn("stddev_pop")
    stderr = NotImplementedSQLFunction()  # TODO: probably can compute in SQL

    # TODO: can't calculate as an aggregate, maybe install some extensions?
    median = NotImplementedSQLFunction()

    min = just_fn("min")
    max = just_fn("max")

    q1 = NotImplementedSQLFunction()
    q3 = NotImplementedSQLFunction()
    ci0 = NotImplementedSQLFunction()
    ci1 = NotImplementedSQLFunction()

    # TODO: need some way to do multi-step aggregates for median, this etc.
    argmin = NotImplementedSQLFunction()
    argmax = NotImplementedSQLFunction()

    def _get_aggregate_function_call_and_alias(self, agg):
        field = agg.field.to_dict() if agg.field != alt.Undefined else None
        call = getattr(self, agg.op.to_dict())(field)
        alias = getattr(agg, "as").to_dict()
        return call, alias

    def transform_aggregate(self, prev: str, transform: alt.AggregateTransform):
        select_list = []
        if transform.groupby != alt.Undefined:
            select_list += transform.groupby
        for agg in transform.aggregate:
            call, alias = self._get_aggregate_function_call_and_alias(agg)
            expr = f'{call} as "{alias}"'
            select_list.append(expr)
        return groupby_query_template.render(
            source=prev, groupby_list=transform.groupby, select_list=select_list
        )

    def transform_sample(self, prev: str, transform: alt.SampleTransform):
        return f"select * from ({prev}) as t order by random() limit {transform.sample}"

    def transform_joinaggregate(self, prev: str, transform: alt.JoinAggregateTransform):
        partition_by = ""
        if transform.groupby != alt.Undefined and len(transform.groupby) > 0:
            partition_list = ", ".join([i.to_dict() for i in transform.groupby])
            partition_by = f"partition by {partition_list}"
        select_list = []
        for agg in transform.joinaggregate:
            call, alias = self._get_aggregate_function_call_and_alias(agg)
            expr = f"{call} over ({partition_by}) as {alias}"
            select_list.append(expr)
        return joinaggregate_query_template.render(source=prev, select_list=select_list)

    def transform_filter(self, prev: str, transform: alt.FilterTransform):
        tree = parser.parse(transform.filter)
        expr = transformer.transform(tree)
        return f"select * from ({prev}) as t where {expr}"
