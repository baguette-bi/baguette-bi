from baguette_bi.mixins import IDMixin


class Client(IDMixin):
    """Knows how to authenticate to a data source and execute queries."""

    def execute(self, query, parameters: dict = None):
        raise NotImplementedError
