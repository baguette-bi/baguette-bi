from unittest.mock import MagicMock

import pytest

from baguette_bi.core.chart import AltairChart, Chart
from baguette_bi.core.context import RenderContext


def test_generate_id():
    assert Chart.id == "baguette_bi.core.chart.Chart"


def test_hash():
    assert hash(Chart) == hash(id(Chart))


def test_raises_not_implemented():
    c = Chart()
    with pytest.raises(NotImplementedError):
        c.render()
    with pytest.raises(NotImplementedError):
        c.rendered_to_dict(None)


def test_altair_rendered_to_dict():
    c = AltairChart()
    obj = MagicMock()
    c.rendered_to_dict(obj)
    assert obj.to_dict.call_count == 1


def test_render_context():
    assert RenderContext({}).parameters == {}
