from baguette_bi.core.data_request import DataRequest

from vega_datasets import data

from .base import Connection


class VegaDatasetsConnection(Connection):
    type: str = "vega_datasets"

    def execute(self, request: DataRequest):
        return getattr(data, request.query)()
