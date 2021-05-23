import altair as alt
from altair import datum
from baguette_bi import bi
from pandas import DataFrame

from .. import datasets, folders


class NormalizedParallelCoordinates(bi.AltairChart):
    folder = folders.other

    def render(self, iris: DataFrame = datasets.iris):
        return (
            alt.Chart(iris)
            .transform_window(index="count()")
            .transform_fold(["petalLength", "petalWidth", "sepalLength", "sepalWidth"])
            .transform_joinaggregate(
                min="min(value)", max="max(value)", groupby=["key"]
            )
            .transform_calculate(
                minmax_value=(datum.value - datum.min) / (datum.max - datum.min),
                mid=(datum.min + datum.max) / 2,
            )
            .mark_line()
            .encode(
                x="key:N",
                y="minmax_value:Q",
                color="species:N",
                detail="index:N",
                opacity=alt.value(0.5),
            )
            .properties(width=500)
        )
