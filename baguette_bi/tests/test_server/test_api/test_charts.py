from unittest import mock

import pytest
from fastapi import HTTPException

from baguette_bi.server.api.charts import render_chart
from baguette_bi.server.project import get_project

project = get_project()


def test_render_chart_raises_404():
    with pytest.raises(HTTPException) as exc:
        render_chart("no such chart", mock.MagicMock(), project=project)
    assert exc.value.status_code == 404
