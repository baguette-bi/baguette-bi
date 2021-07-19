from datetime import date

from baguette_bi.core.data_request import DataRequest


def test_parameters_default():
    req = DataRequest("test")
    assert req.parameters == {}


def test_default_str():
    """Test that DataRequest handles non-JSON serializable values in parameters.
    Parameters are used for generating IDs and improper handling causes an exception."""
    DataRequest("test", {"dt": date(2021, 1, 1)})
