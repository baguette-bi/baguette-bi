import altair as alt
from baguette_bi import bi
from pandas import DataFrame

from .. import datasets, folders


class RidgelinePlot(bi.AltairChart):
    folder = folders.other

    def render(self, seattle_weather: DataFrame = datasets.seattle_weather):
        step = 20
        overlap = 1

        return (
            alt.Chart(seattle_weather, height=step)
            .transform_timeunit(Month="month(date)")
            .transform_joinaggregate(mean_temp="mean(temp_max)", groupby=["Month"])
            .transform_bin(["bin_max", "bin_min"], "temp_max")
            .transform_aggregate(
                value="count()", groupby=["Month", "mean_temp", "bin_min", "bin_max"]
            )
            .transform_impute(
                impute="value", groupby=["Month", "mean_temp"], key="bin_min", value=0
            )
            .mark_area(
                interpolate="monotone",
                fillOpacity=0.8,
                stroke="lightgray",
                strokeWidth=0.5,
            )
            .encode(
                alt.X("bin_min:Q", bin="binned", title="Maximum Daily Temperature (C)"),
                alt.Y(
                    "value:Q", scale=alt.Scale(range=[step, -step * overlap]), axis=None
                ),
                alt.Fill(
                    "mean_temp:Q",
                    legend=None,
                    scale=alt.Scale(domain=[30, 5], scheme="redyellowblue"),
                ),
            )
            .facet(
                row=alt.Row(
                    "Month:T",
                    title=None,
                    header=alt.Header(labelAngle=0, labelAlign="right", format="%B"),
                )
            )
            .properties(title="Seattle Weather", bounds="flush")
            .configure_facet(spacing=0)
            .configure_view(stroke=None)
            .configure_title(anchor="end")
        )
