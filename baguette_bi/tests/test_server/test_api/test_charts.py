from unittest import mock

import pytest
from baguette_bi.server import schema
from baguette_bi.server.api.charts import read_chart, render_chart
from baguette_bi.server.project import project
from fastapi import HTTPException


def test_read_chart_raises_404():
    with pytest.raises(HTTPException) as exc:
        read_chart("no such chart")
    assert exc.value.status_code == 404


def test_read_chart_ok():
    pk = list(project.charts)[0]
    res = read_chart(pk)
    assert isinstance(res, schema.ChartRead)


def test_render_chart_raises_404():
    with pytest.raises(HTTPException) as exc:
        render_chart("no such chart", mock.MagicMock())
    assert exc.value.status_code == 404


def test_render_chart_ok():
    pk = list(project.charts)[0]
    defn = render_chart(pk, mock.MagicMock())
    assert isinstance(defn, dict)
