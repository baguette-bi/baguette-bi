from baguette_bi.connections.query_builders.errors import QueryBuilderError


class SQLCompilationError(QueryBuilderError):
    pass


class SQLExpressionCompilationError(SQLCompilationError):
    pass


class SQLExpressionNotSupportedError(SQLExpressionCompilationError):
    def __init__(self, name):
        super().__init__(f"Expression {name} is not supported yet")


class SQLExpressionIncompatibleError(SQLExpressionCompilationError):
    def __init__(self, name) -> None:
        super().__init__(
            f"Expression {name} has no meaning in SQL, so it's not supported"
        )


class SQLFunctionCompilationError(SQLCompilationError):
    pass


class SQLFunctionNotSupportedError(SQLFunctionCompilationError):
    def __init__(self, name) -> None:
        super().__init__(f"Function {name} is not supported yet")


class SQLFunctionIncompatibleError(SQLFunctionCompilationError):
    def __init__(self, name) -> None:
        super().__init__(
            f"Function {name} has no meaning in SQL, so it's not supported"
        )


def raise_expression_not_supported(name):
    @staticmethod
    def _raise(token):
        raise SQLExpressionNotSupportedError(name)


def raise_expression_incompatible(name):
    @staticmethod
    def _raise(token):
        raise SQLExpressionIncompatibleError(name)


def raise_function_not_supported(name):
    @staticmethod
    def _raise(token):
        raise SQLFunctionNotSupportedError(name)

    return _raise


def raise_function_incompatible(name):
    @staticmethod
    def _raise(token):
        raise SQLFunctionIncompatibleError(name)

    return _raise
