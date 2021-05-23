import altair as alt
from baguette_bi import bi
from pandas import DataFrame
from vega_datasets import data

from .. import folders
from ..datasets import airports, flights_airport


class AirportConnections(bi.AltairChart):
    name = "Connections Among U.S. Airports Interactive"
    folder = folders.case_studies

    def render(
        self,
        airports: DataFrame = airports,
        flights_airport: DataFrame = flights_airport,
    ):
        states = alt.topo_feature(data.us_10m.url, feature="states")

        # Create mouseover selection
        select_city = alt.selection_single(
            on="mouseover", nearest=True, fields=["origin"], empty="none"
        )

        # Define which attributes to lookup from airports.csv
        lookup_data = alt.LookupData(
            airports, key="iata", fields=["state", "latitude", "longitude"]
        )

        background = (
            alt.Chart(states)
            .mark_geoshape(fill="lightgray", stroke="white")
            .properties(width=750, height=500)
            .project("albersUsa")
        )

        connections = (
            alt.Chart(flights_airport)
            .mark_rule(opacity=0.35)
            .encode(
                latitude="latitude:Q",
                longitude="longitude:Q",
                latitude2="lat2:Q",
                longitude2="lon2:Q",
            )
            .transform_lookup(lookup="origin", from_=lookup_data)
            .transform_lookup(
                lookup="destination", from_=lookup_data, as_=["state", "lat2", "lon2"]
            )
            .transform_filter(select_city)
        )

        points = (
            alt.Chart(flights_airport)
            .mark_circle()
            .encode(
                latitude="latitude:Q",
                longitude="longitude:Q",
                size=alt.Size(
                    "routes:Q", scale=alt.Scale(range=[0, 1000]), legend=None
                ),
                order=alt.Order("routes:Q", sort="descending"),
                tooltip=["origin:N", "routes:Q"],
            )
            .transform_aggregate(routes="count()", groupby=["origin"])
            .transform_lookup(lookup="origin", from_=lookup_data)
            .transform_filter((alt.datum.state != "PR") & (alt.datum.state != "VI"))
            .add_selection(select_city)
        )

        return (background + connections + points).configure_view(stroke=None)
