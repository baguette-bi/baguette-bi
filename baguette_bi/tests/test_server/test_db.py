from contextlib import contextmanager
from unittest.mock import MagicMock

from baguette_bi.server.db import get_db


def test_get_db_closes(monkeypatch):
    mgr = contextmanager(get_db)
    Session = MagicMock()
    monkeypatch.setattr("baguette_bi.server.db.Session", Session)
    with mgr():
        pass
    assert Session.return_value.close.call_count == 1
    try:
        with mgr():
            raise Exception
    except Exception:
        assert Session.return_value.close.call_count == 2
