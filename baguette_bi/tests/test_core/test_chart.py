from unittest.mock import MagicMock

import pytest
from baguette_bi.core.chart import AltairChart, Chart
from baguette_bi.core.context import RenderContext
from baguette_bi.core.parameters import TypeInParameter


def test_generate_id():
    assert Chart.id == "d59f0aab40d3942a2b315984d8aeb705"


def test_skip_generate_name():
    assert Chart.name is None
    assert AltairChart.name is None


def test_generate_name():
    class ChartName(Chart):
        pass

    assert ChartName.name == "Chart Name"


def test_add_to_folder_charts():
    class MyChart(Chart):
        folder = MagicMock()

    assert MyChart.folder.charts.append.call_count == 1


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


def test_get_definition_parameters():
    m = MagicMock()

    class TestChart(AltairChart):
        parameters = {
            "x": TypeInParameter(int, "Test", 1),
        }

        def render(self, x: int = 0):
            return m(x=x)

    chart = TestChart()
    chart.get_definition(RenderContext(parameters=chart.parameters))

    assert hasattr(m.call_args, "x")


def test_get_definition_non_existing_parameter():
    class TestChart(AltairChart):
        def render(self, x: int = 0):
            return  # pragma: no cover

    chart = TestChart()
    with pytest.raises(ValueError, match=r"Parameter x not found"):
        chart.get_definition(RenderContext(parameters={}))
