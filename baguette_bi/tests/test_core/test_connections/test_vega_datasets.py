import pandas as pd
from baguette_bi.core.connections.vega_datasets import VegaDatasetsConnection
from baguette_bi.core.data_request import DataRequest


def test_type():
    assert VegaDatasetsConnection.type == "vega_datasets"


def test_execute():
    conn = VegaDatasetsConnection()
    req = DataRequest("cars")
    cars = conn.execute(req)
    assert isinstance(cars, pd.DataFrame)

    templated_req = DataRequest("{{ ds }}", parameters={"ds": "cars"})
    assert conn.execute(templated_req).shape == cars.shape
