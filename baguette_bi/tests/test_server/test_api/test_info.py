from baguette_bi import __version__
from baguette_bi.server.api.info import health, version


def test_version():
    assert version() == {"version": __version__}


def test_health():
    assert health() == {"status": "OK"}
