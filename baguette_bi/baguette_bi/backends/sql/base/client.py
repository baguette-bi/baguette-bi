from baguette_bi.backends.base.client import Client


class SQLClient(Client):
    def __init__(self, **details) -> None:
        super().__init__(**details)
