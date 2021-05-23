import altair as alt
from baguette_bi import bi
from pandas import DataFrame

from .. import datasets, folders


class MarginalHistograms(bi.AltairChart):
    name = "Facetted Scatterplot with marginal histograms"
    folder = folders.other

    def render(self, iris: DataFrame = datasets.iris):
        base = alt.Chart(iris)

        xscale = alt.Scale(domain=(4.0, 8.0))
        yscale = alt.Scale(domain=(1.9, 4.55))

        area_args = {"opacity": 0.3, "interpolate": "step"}

        points = base.mark_circle().encode(
            alt.X("sepalLength:Q", scale=xscale),
            alt.Y("sepalWidth:Q", scale=yscale),
            color="species:N",
        )

        top_hist = (
            base.mark_area(**area_args)
            .encode(
                alt.X(
                    "sepalLength:Q",
                    # when using bins, the axis scale is set through
                    # the bin extent, so we do not specify the scale here
                    # (which would be ignored anyway)
                    bin=alt.Bin(maxbins=20, extent=xscale.domain),
                    stack=None,
                    title="",
                ),
                alt.Y("count()", stack=None, title=""),
                alt.Color("species:N"),
            )
            .properties(height=60)
        )

        right_hist = (
            base.mark_area(**area_args)
            .encode(
                alt.Y(
                    "sepalWidth:Q",
                    bin=alt.Bin(maxbins=20, extent=yscale.domain),
                    stack=None,
                    title="",
                ),
                alt.X("count()", stack=None, title=""),
                alt.Color("species:N"),
            )
            .properties(width=60)
        )

        return top_hist & (points | right_hist)
