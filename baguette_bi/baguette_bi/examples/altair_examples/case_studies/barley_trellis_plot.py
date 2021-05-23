import altair as alt
from pandas import DataFrame

from baguette_bi import bi

from .. import datasets, folders


class BarleyTrellisPlot(bi.AltairChart):
    name = "Becker’s Barley Trellis Plot"
    folder = folders.case_studies

    def render(self, barley: DataFrame = datasets.barley):
        return (
            alt.Chart(barley, title="The Morris Mistake")
            .mark_point()
            .encode(
                alt.X(
                    "yield:Q",
                    title="Barley Yield (bushels/acre)",
                    scale=alt.Scale(zero=False),
                    axis=alt.Axis(grid=False),
                ),
                alt.Y("variety:N", title="", sort="-x", axis=alt.Axis(grid=True)),
                color=alt.Color(
                    "year:N",
                    legend=alt.Legend(title="Year"),
                    scale=alt.Scale(scheme="tableau10"),
                ),
                row=alt.Row(
                    "site:N",
                    title="",
                    sort=alt.EncodingSortField(
                        field="yield", op="sum", order="descending"
                    ),
                ),
            )
            .properties(height=alt.Step(15))
            .configure_view(stroke="transparent")
        )
