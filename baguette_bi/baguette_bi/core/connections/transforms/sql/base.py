import altair as alt
from jinja2 import Template

from baguette_bi.core.connections.transforms.base import BaseTransformMixin
from baguette_bi.core.connections.transforms.sql.utils import (
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


class BaseSQLTransformMixin(BaseTransformMixin):
    """Base ANSI SQL transforms. Basically implements Postgres syntax."""

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

    def transform_aggregate(self, prev: str, transform: alt.AggregateTransform):
        select_list = [] + transform.groupby
        for agg in transform.aggregate:
            field = agg.field.to_dict() if agg.field != alt.Undefined else None
            call = getattr(self, agg.op.to_dict())(field)
            alias = getattr(agg, "as").to_dict()
            expr = f'{call} as "{alias}"'
            select_list.append(expr)
        return groupby_query_template.render(
            source=prev, groupby_list=transform.groupby, select_list=select_list
        )

    def transform_sample(self, prev: str, transform: alt.SampleTransform):
        return f"{prev} limit {transform.sample}"
