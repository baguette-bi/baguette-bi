from unittest.mock import MagicMock

from fastapi.responses import RedirectResponse

from baguette_bi.server.views import post_login


def test_login_post_redirects_to_page():
    request = MagicMock()
    request.url_for.return_value = "/"
    request.session.pop.return_value = "/test"
    res = post_login(request)
    assert isinstance(res, RedirectResponse)
    assert res.status_code == 302
    assert res.headers["Location"] == "/test"
