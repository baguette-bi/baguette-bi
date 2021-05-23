import altair as alt
from baguette_bi import bi
from pandas import DataFrame

from .. import datasets, folders


class BinnedHeatmap(bi.AltairChart):
    folder = folders.other

    def render(self, movies: DataFrame = datasets.movies):
        return (
            alt.Chart(movies)
            .mark_rect()
            .encode(
                alt.X("IMDB_Rating:Q", bin=alt.Bin(maxbins=60)),
                alt.Y("Rotten_Tomatoes_Rating:Q", bin=alt.Bin(maxbins=40)),
                alt.Color("count(IMDB_Rating):Q", scale=alt.Scale(scheme="greenblue")),
            )
        )
