from unittest import mock

import pytest
from fastapi import HTTPException

from baguette_bi.core import User
from baguette_bi.server import schema
from baguette_bi.server.api.charts import read_chart, render_chart
from baguette_bi.server.project import get_project

admin = User("admin", is_admin=True)
project = get_project()


def test_read_chart_raises_404():
    with pytest.raises(HTTPException) as exc:
        read_chart("no such chart", project=project, user=admin)
    assert exc.value.status_code == 404


def test_read_chart_ok():
    pk = list(project.charts)[0]
    res = read_chart(pk, project=project, user=admin)
    assert isinstance(res, schema.ChartRead)


def test_render_chart_raises_404():
    with pytest.raises(HTTPException) as exc:
        render_chart("no such chart", mock.MagicMock(), project=project, user=admin)
    assert exc.value.status_code == 404


def test_render_chart_ok():
    pk = list(project.charts)[0]
    defn = render_chart(pk, mock.MagicMock(), project=project, user=admin)
    assert isinstance(defn, dict)
