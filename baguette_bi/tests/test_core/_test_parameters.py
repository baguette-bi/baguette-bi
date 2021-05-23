from datetime import date
from unittest.mock import MagicMock

import pytest
from baguette_bi.core.parameters import (
    ListParameterMixin,
    MultipleChoiceParameter,
    Parameter,
    SingleChoiceParameter,
    TypeInListParameter,
    TypeInParameter,
)


def test_type_not_allowed():
    with pytest.raises(TypeError, match=r"^Supported types for parameters are"):
        Parameter(dict, "test", {})


def test_value_getter():
    assert Parameter(int, "test", 0).value == 0


def test_value_setter():
    with pytest.raises(ValueError):
        Parameter(int, "test", "a")


def test_options_converted():
    par = SingleChoiceParameter(int, "test", ["0", "1", "2"], "0")
    assert par.options == [0, 1, 2]


def test_list_parameter_value_converted():
    par = MultipleChoiceParameter(int, "test", [0, 1, 2], ["0", "1"])
    assert par.value == [0, 1]


def test_type_in_value_converted():
    par = TypeInParameter(int, "test", "0")
    assert par.value == 0


def test_type_in_list_value_converted():
    par = TypeInListParameter(int, "test", ["0", "1"])
    assert par.value == [0, 1]
