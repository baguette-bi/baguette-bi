import altair as alt
from baguette_bi import bi
from pandas import DataFrame

from .. import datasets, folders


class UsPopulationWrappedFacet(bi.AltairChart):
    name = "US Population: Wrapped Facet"
    folder = folders.case_studies

    def render(self, population: DataFrame = datasets.population):
        return (
            alt.Chart(population)
            .mark_area()
            .encode(
                x="age:O",
                y=alt.Y(
                    "sum(people):Q", title="Population", axis=alt.Axis(format="~s")
                ),
                facet=alt.Facet("year:O", columns=5),
            )
            .properties(title="US Age Distribution By Year", width=90, height=80)
        )
