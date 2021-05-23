from baguette_bi.core.chart import Chart, ChartMeta
from baguette_bi.core.context import RenderContext


def test(chart_cls: ChartMeta, **kwargs):
    chart: Chart = chart_cls()
    return chart.get_rendered(RenderContext(parameters=kwargs))
