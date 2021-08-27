from unittest.mock import MagicMock

from baguette_bi.core.chart import AltairChart
from baguette_bi.core.context import RenderContext


def test_generate_id():
    assert AltairChart.id == "baguette_bi.core.chart:AltairChart"


def test_altair_rendered_to_dict():
    class TestChart(AltairChart):
        def render(self):
            pass

    c = TestChart()
    obj = MagicMock()
    c.rendered_to_dict(obj)
    assert obj.to_dict.call_count == 1


def test_render_context():
    assert RenderContext({}).parameters == {}
