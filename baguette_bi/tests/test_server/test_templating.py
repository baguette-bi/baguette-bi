from types import SimpleNamespace

from baguette_bi.server.templating import set_params


def test_set_params_context_no_mutation():
    ctx = {"params": SimpleNamespace(param=1), "current_page": "current"}
    set_params(ctx, "test", param=2)
    assert ctx["params"].param == 1
