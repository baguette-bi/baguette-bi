import altair as alt
import pandas as pd

from baguette_bi import bi
from baguette_bi.examples.docs.datasets import AnyVegaDataset, Cars


class CarsHorsePowerHistogram(bi.AltairChart):
    def render(self, cars: pd.DataFrame = Cars):
        return (
            alt.Chart(cars)
            .mark_bar()
            .encode(x=alt.X("Horsepower:Q", bin=True), y="count()")
        )


class CarsColumnHistogram(bi.AltairChart):
    def render(self, column: str, cars: pd.DataFrame = Cars):
        return (
            alt.Chart(cars)
            .mark_bar()
            .encode(x=alt.X(f"{column}:Q", bin=True), y="count()")
        )


class AnyVegaDatasetColumnHistogram(bi.AltairChart):
    def render(self, column: str, df: pd.DataFrame = AnyVegaDataset):
        return (
            alt.Chart(df)
            .mark_bar()
            .encode(x=alt.X(f"{column}:Q", bin=True), y="count()")
        )
