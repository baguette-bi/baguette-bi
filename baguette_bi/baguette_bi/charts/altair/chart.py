from baguette_bi.charts.base import Chart


class AltairChart(Chart):
    rendering_engine: str = "vega-lite"

    def rendered_to_dict(self, obj):
        return obj.to_dict()
