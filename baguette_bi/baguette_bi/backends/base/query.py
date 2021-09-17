from typing import Any, Dict, List, Optional

import altair as alt
from jinja2 import Template

from baguette_bi.backends.base.client import Client
from baguette_bi.charts.altair.expr.parser import parser

transform_mapping = {
    alt.AggregateTransform: "transform_aggregate",
    alt.BinTransform: "transform_bin",
    alt.CalculateTransform: "transform_calculate",
    alt.DensityTransform: "transform_density",
    alt.FilterTransform: "transform_filter",
    alt.FlattenTransform: "transform_flatten",
    alt.FoldTransform: "transform_fold",
    alt.ImputeTransform: "transform_impute",
    alt.JoinAggregateTransform: "transform_joinaggregate",
    alt.LookupTransform: "transform_lookup",
    alt.LoessTransform: "transform_loess",
    alt.PivotTransform: "transform_pivot",
    alt.QuantileTransform: "transform_quantile",
    alt.RegressionTransform: "transform_regression",
    alt.SampleTransform: "transform_sample",
    alt.StackTransform: "transform_stack",
    alt.TimeUnitTransform: "transform_timeunit",
    alt.WindowTransform: "transform_window",
}


class Query:
    """Queries are backend-specific."""

    def __init__(
        self,
        client: Client,
        base: Any,
        parameters: Optional[Dict] = None,
        transforms: Optional[List] = None,
        echo: bool = False,
    ):
        self.client = client
        self.base = base
        self.parameters = parameters
        self.transforms = transforms
        self.echo = echo

    def build(self):
        """Build the final query suitable for execution on the client."""
        query = Template(self.base).render(**self.parameters)
        for transform in self.transforms:
            transform_method = getattr(self, transform_mapping[transform.__class__])
            try:
                query = transform_method(query, transform)
            except NotImplementedError:
                raise NotImplementedError(
                    f"{transform.__class__.__name__} "
                    "is not implemented for {self.__class__.__name__}"
                )
        return query

    def execute(self):
        """Build and execute self on the client."""
        built_query = self.build()
        if self.echo:
            print(built_query)
        return self.client.execute(built_query, self.parameters)

    def parse_expression(self, expr: str):
        return parser.parse(expr)

    def transform_aggregate(self, prev: Any, transform: alt.AggregateTransform):
        raise NotImplementedError

    def transform_bin(self, prev: Any, transform: alt.BinTransform):
        raise NotImplementedError

    def transform_calculate(self, prev: Any, transform: alt.CalculateTransform):
        raise NotImplementedError

    def transform_density(self, prev: Any, transform: alt.DensityTransform):
        raise NotImplementedError

    def transform_filter(self, prev: Any, transform: alt.FilterTransform):
        raise NotImplementedError

    def transform_flatten(self, prev: Any, transform: alt.FlattenTransform):
        raise NotImplementedError

    def transform_fold(self, prev: Any, transform: alt.FoldTransform):
        raise NotImplementedError

    def transform_impute(self, prev: Any, transform: alt.ImputeTransform):
        raise NotImplementedError

    def transform_joinaggregate(self, prev: Any, transform: alt.JoinAggregateTransform):
        raise NotImplementedError

    def transform_lookup(self, prev: Any, transform: alt.LookupTransform):
        raise NotImplementedError

    def transform_loess(self, prev: Any, transform: alt.LoessTransform):
        raise NotImplementedError

    def transform_pivot(self, prev: Any, transform: alt.PivotTransform):
        raise NotImplementedError

    def transform_quantile(self, prev: Any, transform: alt.QuantileTransform):
        raise NotImplementedError

    def transform_regression(self, prev: Any, transform: alt.RegressionTransform):
        raise NotImplementedError

    def transform_sample(self, prev: Any, transform: alt.SampleTransform):
        raise NotImplementedError

    def transform_stack(self, prev: Any, transform: alt.StackTransform):
        raise NotImplementedError

    def transform_timeunit(self, prev: Any, transform: alt.TimeUnitTransform):
        raise NotImplementedError

    def transform_window(self, prev: Any, transform: alt.WindowTransform):
        raise NotImplementedError
