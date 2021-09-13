from vega_datasets import data

from baguette_bi.connections.base import Connection


class VegaDatasetsConnection(Connection):
    type: str = "vega_datasets"

    def execute(self, query, parameters):
        return getattr(data, query)()
