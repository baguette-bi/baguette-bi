from unittest.mock import MagicMock

from fastapi.responses import RedirectResponse

from baguette_bi.server.views import post_login


def test_login_post_redirects_to_root():
    request = MagicMock()
    request.url_for.return_value = "/"
    res = post_login(request)
    assert isinstance(res, RedirectResponse)
    assert res.status_code == 302
    assert res.headers["Location"] == "/"
