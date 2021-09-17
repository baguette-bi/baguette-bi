from baguette_bi.connections.query_builders.utils import determine_bin_size


def test_determine_bin_size():
    """Test cases are generated from js implementation results.
    This is really not exhaustive and should be updated by someone who understands
    the underlying algo :-/
    """
    assert determine_bin_size([32, 994]) == (0, 1000, 100)
    assert determine_bin_size([32, 994], step=68) == (0, 1020, 68)
    assert determine_bin_size([32, 995], maxbins=5) == (0, 1000, 200)
    assert determine_bin_size([32, 995], base=3) == (0, 1093.5, 121.5)
