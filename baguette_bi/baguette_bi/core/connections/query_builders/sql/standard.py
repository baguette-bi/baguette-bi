import altair as alt
from jinja2 import Template

from baguette_bi.core.connections.query_builders.sql.base import BaseSQLQueryBuilder
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
        select_list = [] + transform.groupby
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
