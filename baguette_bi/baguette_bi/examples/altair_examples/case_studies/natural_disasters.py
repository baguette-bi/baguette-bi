import altair as alt
from baguette_bi import bi
from pandas import DataFrame

from .. import datasets, folders


class NaturalDisasters(bi.AltairChart):
    folder = folders.case_studies

    def render(self, disasters: DataFrame = datasets.disasters):
        return (
            alt.Chart(disasters)
            .mark_circle(opacity=0.8, stroke="black", strokeWidth=1)
            .encode(
                alt.X("Year:O", axis=alt.Axis(labelAngle=0, labelOverlap=True)),
                alt.Y("Entity:N"),
                alt.Size(
                    "Deaths:Q",
                    scale=alt.Scale(range=[0, 4000]),
                    legend=alt.Legend(title="Annual Global Deaths"),
                ),
                alt.Color("Entity:N", legend=None),
            )
            .properties(width=900, height=600)
            .transform_filter(alt.datum.Entity != "All natural disasters")
        )
