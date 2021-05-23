from datetime import date, datetime, time, timedelta
from typing import Callable, List, Type, Union

from pydantic.datetime_parse import (
    parse_date,
    parse_datetime,
    parse_duration,
    parse_time,
)

allowed_types = {
    "bool": bool,
    "int": int,
    "float": float,
    "str": str,
    "date": parse_date,
    "datetime": parse_datetime,
    "time": parse_time,
    "timedelta": parse_duration,
}
type_names = ", ".join(t for t in allowed_types)

Value = Union[bool, int, float, str, time, date, datetime, timedelta]

ValueOrCallable = Union[Value, Callable[[], Value]]
ListOrCallable = Union[List[Value], Callable[[], List[Value]]]


class Parameter:
    def __init__(self, T: Type, title: str, default: ValueOrCallable):
        if not isinstance(T, type):
            raise ValueError("T must be a type")
        T = T.__name__
        if T not in allowed_types:
            raise TypeError(
                f"Supported types for parameters are {type_names}," f" got {T} instead"
            )
        self.T = T
        self.title = title
        self.default_value = default if callable(default) else lambda: default
        self.value  # validate

    @property
    def value(self):
        _conv = allowed_types[self.T]
        return _conv(self.default_value())


class ChoiceParameter(Parameter):
    def __init__(
        self,
        T: Type,
        title: str,
        options: ListOrCallable,
        default: Union[ValueOrCallable, ListOrCallable],
    ):
        super().__init__(T, title, default)
        self.default_options = options if callable(options) else lambda: options

    @property
    def options(self):
        _conv = allowed_types[self.T]
        return [_conv(o) for o in self.default_options()]


class SingleChoiceParameter(ChoiceParameter):
    def __init__(
        self, T: Type, title: str, options: ListOrCallable, default: ValueOrCallable
    ):
        super().__init__(T, title, options, default)


class ListParameterMixin:
    @property
    def value(self):
        _conv = allowed_types[self.T]
        return [_conv(v) for v in self.default_value()]


class MultipleChoiceParameter(ListParameterMixin, ChoiceParameter):
    def __init__(
        self, T: Type, title: str, options: ListOrCallable, default: ListOrCallable
    ):
        super().__init__(T, title, options, default)


class TypeInParameter(Parameter):
    def __init__(self, T: Type, title: str, default: ValueOrCallable):
        super().__init__(T, title, default)


class TypeInListParameter(ListParameterMixin, Parameter):
    def __init__(self, T: Type, title: str, default: ListOrCallable):
        super().__init__(T, title, default)
