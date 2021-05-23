import altair as alt
from baguette_bi import bi
from pandas import DataFrame

from .. import datasets, folders


class OneDotPerZipcode(bi.AltairChart):
    folder = folders.case_studies

    def render(self, zipcodes: DataFrame = datasets.zipcodes):
        return (
            alt.Chart(zipcodes)
            .transform_calculate(
                "leading digit", alt.expr.substring(alt.datum.zip_code, 0, 1)
            )
            .mark_circle(size=3)
            .encode(
                longitude="longitude:Q",
                latitude="latitude:Q",
                color="leading digit:N",
                tooltip="zip_code:N",
            )
            .project(type="albersUsa")
            .properties(width=650, height=400)
        )
