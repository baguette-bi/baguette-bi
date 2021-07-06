import altair as alt
from vega_datasets import data

from baguette_bi import bi

source = data.iowa_electricity()


class MyChart(bi.AltairChart):
    def render(self):
        return (
            alt.Chart(source)
            .mark_area()
            .encode(x="year:T", y="net_generation:Q", color="source:N")
        )
