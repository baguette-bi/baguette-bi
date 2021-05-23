from typing import Any, List, Literal, Optional, Union

from baguette_bi.core.parameters import allowed_types
from pydantic import validator

from .base import Base


class BaseParameter(Base):
    type: Literal[None] = None
    T: str
    title: str
    value: Any

    @validator("T", pre=True)
    def validate_T(cls, value):
        return value

    @validator("value")
    def convert_value(cls, value, values):
        T = values["T"]
        if isinstance(value, T):
            return value
        return allowed_types[T](value)


class ChoiceParameter(BaseParameter):
    options: List

    @validator("options")
    def convert_options(cls, value, values):
        T = values["T"]
        result = []
        for o in value:
            if isinstance(o, T):
                result.append(o)
                continue
            result.append(allowed_types[T](o))
        return result


class ListParameterMixin(BaseParameter):
    value: List

    @validator("value")
    def convert_value(cls, value, values):
        T = values["T"]
        result = []
        for v in value:
            if isinstance(v, T):
                result.append(v)
                continue
            result.append(allowed_types[T](v))
        return result


class SingleChoiceParameter(ChoiceParameter):
    type: Literal["single_choice"] = "single_choice"


class MultipleChoiceParameter(ListParameterMixin, ChoiceParameter):
    type: Literal["multiple_choice"] = "multiple_choice"


class TypeInParameter(BaseParameter):
    type: Literal["type_in"] = "type_in"
    value: Optional[Any] = None

    @validator("value")
    def convert_value(cls, value, values):
        if value is None:
            return value
        T = values["T"]
        if isinstance(value, T):
            return value
        return allowed_types[T](value)


class TypeInListParameter(ListParameterMixin, BaseParameter):
    type: Literal["type_in_list"] = "type_in_list"
    value: List = []


Parameter = Union[
    SingleChoiceParameter, MultipleChoiceParameter, TypeInParameter, TypeInListParameter
]
