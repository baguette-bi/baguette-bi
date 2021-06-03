from fastapi.responses import RedirectResponse

from baguette_bi.server.views import post_login


def test_login_post_redirects_to_root():
    res = post_login()
    assert isinstance(res, RedirectResponse)
    assert res.status_code == 302
    assert res.headers["Location"] == "/"
