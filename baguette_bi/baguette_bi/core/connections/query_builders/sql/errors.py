from baguette_bi.core.connections.query_builders.errors import QueryBuilderError


class SQLCompilationError(QueryBuilderError):
    pass


class SQLExpressionCompilationError(SQLCompilationError):
    """When Vega expression doesn't make sense in SQL and can't be translated."""

    def __init__(self, name):
        super().__init__(
            f"Expression {name} makes no sense in SQL and can't be compiled."
        )


class SQLFunctionCompilationError(SQLCompilationError):
    def __init__(self, name):
        super().__init__(f"Function {name} makes no sense in SQL or is not supported.")
