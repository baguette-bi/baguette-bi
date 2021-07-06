from vega_datasets import data

from baguette_bi.core.connections.base import Connection
from baguette_bi.core.data_request import DataRequest


class VegaDatasetsConnection(Connection):
    type: str = "vega_datasets"

    def execute(self, request: DataRequest):
        return getattr(data, request.query)()
