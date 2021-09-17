import altair as alt
from jinja2 import Template

from baguette_bi.backends.base.query import Query
from baguette_bi.backends.sql.base.aggregate import AggregateFunctionCompiler
from baguette_bi.backends.sql.base.compiler import SQLCompiler, SQLFunctionCompiler
from baguette_bi.backends.utils import determine_bin_size


class SQLAggregateFunctionCompiler(SQLFunctionCompiler):
    """A secondary function compiler that translates Vega aggregate functions into SQL."""


groupby_template = Template(
    """
select {{ ", ".join(select_list) }}
from ({{ source }}) as t
{% if groupby_list %}
group by {{ ", ".join(groupby_list) }}
{% endif %}
"""
)

select_list_template = Template(
    """
select *, {{ ", ".join(select_list) }}
from ({{ source }}) as t
"""
)

bin_defaults = dict(
    anchor=None,
    base=10,
    divide=[5, 2],
    maxbins=10,
    minstep=0,
    nice=True,
    step=None,
    steps=None,
)


class SQLQuery(Query):
    """Most SQL syntax is standard, so query implementations will only differ in
    expression compilers.
    """

    compiler = SQLCompiler()
    aggregate_function_compiler = AggregateFunctionCompiler()

    def transform_sample(self, prev: str, transform: alt.SampleTransform):
        return f"select * from ({prev}) as t order by random() limit {transform.sample}"

    def transform_filter(self, prev: str, transform: alt.FilterTransform):
        tree = self.parse_expression(transform.filter)
        expr = self.compiler.compile(tree)
        return f"select * from ({prev}) as t where {expr}"

    def transform_calculate(self, prev: str, transform: alt.CalculateTransform):
        alias = getattr(transform, "as").to_dict()
        expr = self.compiler.compile(self.parse_expression(transform.calculate))
        return f"select *, {expr} as {alias} from ({prev}) as t"

    def _get_aggregate_function_call_and_alias(self, agg):
        field = agg.field.to_dict() if agg.field != alt.Undefined else None
        call = getattr(self.aggregate_function_compiler, agg.op.to_dict())([field])
        alias = getattr(agg, "as").to_dict()
        return call, alias

    def transform_aggregate(self, prev: str, transform: alt.AggregateTransform):
        select_list = []
        groupby_list = []
        if transform.groupby != alt.Undefined:
            groupby_list = transform.groupby
            select_list += groupby_list
        for agg in transform.aggregate:
            call, alias = self._get_aggregate_function_call_and_alias(agg)
            expr = f'{call} as "{alias}"'
            select_list.append(expr)
        return groupby_template.render(
            source=prev, groupby_list=groupby_list, select_list=select_list
        )

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
        return select_list_template.render(source=prev, select_list=select_list)

    def _get_bin_aliases(self, transform: alt.BinTransform):
        alias = getattr(transform, "as")
        if isinstance(alias, alt.FieldName):
            f = alias.to_dict()
            return f, f"{f}_end"
        b0, b1 = alias
        return b0.to_dict(), b1.to_dict()

    def transform_bin(self, prev: str, transform: alt.BinTransform):
        field = transform.field.to_dict()
        # determine extent
        query = self.transform_aggregate(
            prev,
            alt.AggregateTransform.from_dict(
                {
                    "aggregate": [
                        {"op": "min", "field": field, "as": "min_extent"},
                        {"op": "max", "field": field, "as": "max_extent"},
                    ]
                }
            ),
        )
        if self.echo:
            print(query)
        _, start, stop = next(self.client.execute(query, self.parameters).itertuples())
        # determine bin size
        bin_params = {}
        bin_params.update(bin_defaults)
        if isinstance(transform.bin, alt.BinParams):
            bin_params.update(transform.bin.to_dict())
        start, stop, step = determine_bin_size([start, stop], **bin_params)
        b0, b1 = self._get_bin_aliases(transform)
        # floor((v - start) / step) * step + start
        # bin is just a series of calculations
        c0 = self.transform_calculate(
            prev,
            alt.CalculateTransform.from_dict(
                {
                    "calculate": (
                        f"round((datum['{field}'] - {start}) / {step}) "
                        f"* {step} + {start}"
                    ),
                    "as": b0,
                }
            ),
        )
        return self.transform_calculate(
            c0,
            alt.CalculateTransform.from_dict(
                {"calculate": f"datum['{b0}'] + {step}", "as": b1}
            ),
        )
