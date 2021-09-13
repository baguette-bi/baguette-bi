from typing import Any, Dict, List, Optional

import altair as alt
from jinja2 import Template

from baguette_bi.connections.query_builders.errors import (
    UnsupportedTransformQueryBuilderError,
)


class BaseQueryBuilder:
    def __init__(self):
        self.transform_mapping = {
            alt.AggregateTransform: self.transform_aggregate,
            alt.BinTransform: self.transform_bin,
            alt.CalculateTransform: self.transform_calculate,
            alt.DensityTransform: self.transform_density,
            alt.FilterTransform: self.transform_filter,
            alt.FlattenTransform: self.transform_flatten,
            alt.FoldTransform: self.transform_fold,
            alt.ImputeTransform: self.transform_impute,
            alt.JoinAggregateTransform: self.transform_joinaggregate,
            alt.LookupTransform: self.transform_lookup,
            alt.LoessTransform: self.transform_loess,
            alt.PivotTransform: self.transform_pivot,
            alt.QuantileTransform: self.transform_quantile,
            alt.RegressionTransform: self.transform_regression,
            alt.SampleTransform: self.transform_sample,
            alt.StackTransform: self.transform_stack,
            alt.TimeUnitTransform: self.transform_timeunit,
            alt.WindowTransform: self.transform_window,
        }

    def build(
        self,
        query: Any,
        parameters: Optional[Dict[str, Any]] = None,
        transforms: Optional[List[alt.Transform]] = None,
    ):
        query = Template(query).render(**parameters)
        for transform in transforms:
            query = self.execute_transform(query, transform)
        return query

    def execute_transform(self, prev: Any, transform: alt.Transform):
        transform_function = self.transform_mapping.get(transform.__class__)
        return transform_function(prev, transform)

    def transform_aggregate(self, prev: Any, transform: alt.AggregateTransform):
        raise UnsupportedTransformQueryBuilderError(self, "aggregate")

    def transform_bin(self, prev: Any, transform: alt.BinTransform):
        raise UnsupportedTransformQueryBuilderError(self, "bin")

    def transform_calculate(self, prev: Any, transform: alt.CalculateTransform):
        raise UnsupportedTransformQueryBuilderError(self, "calculate")

    def transform_density(self, prev: Any, transform: alt.DensityTransform):
        raise UnsupportedTransformQueryBuilderError(self, "density")

    def transform_filter(self, prev: Any, transform: alt.FilterTransform):
        raise UnsupportedTransformQueryBuilderError(self, "filter")

    def transform_flatten(self, prev: Any, transform: alt.FlattenTransform):
        raise UnsupportedTransformQueryBuilderError(self, "flatten")

    def transform_fold(self, prev: Any, transform: alt.FoldTransform):
        raise UnsupportedTransformQueryBuilderError(self, "fold")

    def transform_impute(self, prev: Any, transform: alt.ImputeTransform):
        raise UnsupportedTransformQueryBuilderError(self, "impute")

    def transform_joinaggregate(self, prev: Any, transform: alt.JoinAggregateTransform):
        raise UnsupportedTransformQueryBuilderError(self, "joinaggregate")

    def transform_lookup(self, prev: Any, transform: alt.LookupTransform):
        raise UnsupportedTransformQueryBuilderError(self, "lookup")

    def transform_loess(self, prev: Any, transform: alt.LoessTransform):
        raise UnsupportedTransformQueryBuilderError(self, "loess")

    def transform_pivot(self, prev: Any, transform: alt.PivotTransform):
        raise UnsupportedTransformQueryBuilderError(self, "pivot")

    def transform_quantile(self, prev: Any, transform: alt.QuantileTransform):
        raise UnsupportedTransformQueryBuilderError(self, "quantile")

    def transform_regression(self, prev: Any, transform: alt.RegressionTransform):
        raise UnsupportedTransformQueryBuilderError(self, "regression")

    def transform_sample(self, prev: Any, transform: alt.SampleTransform):
        raise UnsupportedTransformQueryBuilderError(self, "sample")

    def transform_stack(self, prev: Any, transform: alt.StackTransform):
        raise UnsupportedTransformQueryBuilderError(self, "stack")

    def transform_timeunit(self, prev: Any, transform: alt.TimeUnitTransform):
        raise UnsupportedTransformQueryBuilderError(self, "timeunit")

    def transform_window(self, prev: Any, transform: alt.WindowTransform):
        raise UnsupportedTransformQueryBuilderError(self, "window")
