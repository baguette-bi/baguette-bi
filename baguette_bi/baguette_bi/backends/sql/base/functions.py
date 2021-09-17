from typing import Collection, Optional, Union


class SQLFunction:
    """A callable descriptor that will return an appropriate SQL function call rendered
    as a string when called. If name argument is None, function name will be the same
    as in Vega, if nargs is not None, the function will check that the user-provided
    number of arguments at compile time.
    """

    check_nargs = True

    def __init__(
        self,
        name: Optional[str] = None,
        nargs: Optional[Union[int, Collection[int]]] = 1,
    ):
        self._name = name
        self.nargs = nargs

    def __init_subclass__(cls):
        """Call check_nargs before the main call."""
        call = cls.__call__

        def wrapped(self, args):
            if cls.check_nargs:
                self.check_nargs(args)
            return call(self, args)

        cls.__call__ = wrapped

    @property
    def name(self):
        return self._name if self._name is not None else self.vega_name

    def __set_name__(self, instance, name):
        self.vega_name = name

    def __get__(self, obj, objtype=None):
        return self

    def check_nargs(self, args):
        args = len(args)
        if self.nargs is not None:
            raise_ = False
            if isinstance(self.nargs, int):
                raise_ = args != self.nargs
            elif args not in self.nargs:
                raise_ = True
            if raise_:
                raise ValueError(
                    f"Function {self.vega_name} expects {self.nargs} arguments, got {args}"
                )

    @staticmethod
    def defaults(args: list, nargs: int, defaults: list):
        """Given a list of args, pad default values to the right."""
        if len(args) == nargs:
            return args
        n = nargs - len(args)
        return args + defaults[:-n]

    def __call__(self, args):
        self.check_nargs(args)
        return f"{self.name}({', '.join(args)})"


class NotImplementedSQLFunction(SQLFunction):
    def __call__(self, args):
        raise NotImplementedError(
            f"Function {self.vega_name} is not implemented for this backend"
        )


class CastSQLFunction(SQLFunction):
    def __init__(self, as_type: str):
        super().__init__("cast", 1)
        self.as_type = as_type

    def __call__(self, args):
        return f"cast({args[0]} as {self.as_type})"


class ClampSQLFunction(SQLFunction):
    def __init__(self):
        super().__init__(name="clamp", nargs=3)

    def __call__(self, args):
        v, s, e = args
        return f"case when {v} < {s} then {s} when {v} > {e} then {e} else {v} end"


class ExtractSQLFunction(SQLFunction):
    def __init__(self, part: str):
        super().__init__(name="extract", nargs=1)
        self.part = part

    def __call__(self, args):
        return f"{self.name}({self.part} from {args[0]})"


class PadSQLFunction(SQLFunction):
    """Normal pad is not supported by most SQL engines. Chooses lpad or rpad based on
    the arguments.
    """

    def __init__(self):
        super().__init__(name="pad", nargs={2, 3, 4})

    def __call__(self, args):
        args = self.defaults(args, 4, ["' '", "'right'"])
        string, length, character, align = args
        name = "lpad" if align == "'right'" else "lpad"
        if align == "'center'":
            raise ValueError(
                f"Center align is not supported by {self.vega_name} in SQL."
            )
        return f"{name}({string}, {length}, {character})"


class SubstrSQLFunction(SQLFunction):
    """Translates slice(s, start, end) to substr(s, from, count). Default function name
    is substr, but can be changed.
    """

    def __init__(self, name: str = "substr"):
        super().__init__(name=name, nargs=3)

    def __call__(self, args):
        string, start, stop = args
        if stop < start:
            raise ValueError("SQL doesn't support negative slicing")
        length = f"lenth({string})"
        # substr is 1-based
        return f"{self.name}({string}, {start} + 1, {length} - {stop})"


class TruncateSQLFunction(SQLFunction):
    """Translates truncate Vega function into SQL's LEFT() or RIGHT()."""

    def __init__(self):
        super().__init__(name=None, nargs={2, 3, 4})

    def __call__(self, args):
        args = self.defaults(args, 4, ["'right'", "'…'"])
        string, length, align, _ = args
        name = "left" if align == "'right'" else "right"
        return f"{name}({string}, {length})"  # TODO: support ellipsis


class TernarySQLFunction(SQLFunction):
    def __init__(self):
        super().__init__(nargs=3)

    def __call__(self, args):
        condition, a, b = args
        return f"case when {condition} then {a} else {b}"
