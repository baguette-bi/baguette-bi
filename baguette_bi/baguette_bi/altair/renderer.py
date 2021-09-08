import altair as alt

from baguette_bi.altair.preprocess import extract_inline_transforms
from baguette_bi.core.context import RenderContext
from baguette_bi.core.dataset import Dataset

VEGALITE_VERSION = alt.schema.SCHEMA_VERSION.lstrip("v")
VEGA_VERSION = "5"
VEGAEMBED_VERSION = "6"


class DataTransformRenderer(alt.utils.display.HTMLRenderer):
    def transform_spec(self, spec: dict) -> dict:
        chart = alt.Chart.from_dict(spec)
        chart = extract_inline_transforms(chart)
        dataset = Dataset.main_registry.get(chart.data.name)()
        transforms = None
        if chart.transform != alt.Undefined:
            transforms = chart.transform
            chart.transform = alt.Undefined
        # TODO: have a way to provide context interactively
        data = dataset.get_data(RenderContext(), transforms)
        if chart.datasets == alt.Undefined:
            chart["datasets"] = {}
        chart.datasets[chart.data.name] = data.to_dict(orient="records")
        return chart.to_dict()

    def __call__(self, spec, **metadata):
        return super().__call__(self.transform_spec(spec), **metadata)


data_transform_renderer = DataTransformRenderer(
    mode="vega-lite",
    template="universal",
    vega_version=VEGA_VERSION,
    vegaembed_version=VEGAEMBED_VERSION,
    vegalite_version=VEGALITE_VERSION,
)
