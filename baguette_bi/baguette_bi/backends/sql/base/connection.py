from baguette_bi.backends.base.connection import Connection


class SQLConnection(Connection):
    def __init__(self, client):
        super().__init__(client)
