class QueryBuilderError(Exception):
    pass


class UnsupportedTransformQueryBuilderError(QueryBuilderError):
    def __init__(self, obj, transform: str):
        super().__init__(
            f"{obj.__class__.__name__}: {transform} transform is not supported."
        )
