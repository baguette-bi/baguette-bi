from baguette_bi.core.data_request import DataRequest


def test_parameters_default():
    req = DataRequest("test")
    assert req.parameters == {}
