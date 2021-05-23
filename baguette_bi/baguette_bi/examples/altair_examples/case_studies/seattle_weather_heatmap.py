import altair as alt
from baguette_bi import bi
from pandas import DataFrame

from .. import datasets, folders


class SeattleWeatherHeatmap(bi.AltairChart):
    folder = folders.case_studies

    def render(self, seattle_temps: DataFrame = datasets.seattle_temps):
        return (
            alt.Chart(
                seattle_temps, title="2010 Daily High Temperature (F) in Seattle, WA"
            )
            .mark_rect()
            .encode(
                x="date(date):O",
                y="month(date):O",
                color=alt.Color("max(temp):Q", scale=alt.Scale(scheme="inferno")),
                tooltip=[
                    alt.Tooltip("monthdate(date):T", title="Date"),
                    alt.Tooltip("max(temp):Q", title="Max Temp"),
                ],
            )
            .properties(width=550)
        )
