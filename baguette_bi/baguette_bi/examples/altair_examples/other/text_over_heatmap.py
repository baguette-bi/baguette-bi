import altair as alt
from baguette_bi import bi
from pandas import DataFrame

from .. import datasets, folders


class TextOverAHeatmap(bi.AltairChart):
    folder = folders.other

    def render(self, cars: DataFrame = datasets.cars):
        base = (
            alt.Chart(cars)
            .transform_aggregate(num_cars="count()", groupby=["Origin", "Cylinders"])
            .encode(
                alt.X("Cylinders:O", scale=alt.Scale(paddingInner=0)),
                alt.Y("Origin:O", scale=alt.Scale(paddingInner=0)),
            )
        )

        # Configure heatmap
        heatmap = base.mark_rect().encode(
            color=alt.Color(
                "num_cars:Q",
                scale=alt.Scale(scheme="viridis"),
                legend=alt.Legend(direction="horizontal"),
            )
        )

        # Configure text
        text = base.mark_text(baseline="middle").encode(
            text="num_cars:Q",
            color=alt.condition(
                alt.datum.num_cars > 100, alt.value("black"), alt.value("white")
            ),
        )

        # Draw the chart
        return heatmap + text
