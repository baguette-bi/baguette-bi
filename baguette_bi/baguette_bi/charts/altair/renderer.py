from concurrent.futures import ThreadPoolExecutor

import altair as alt

from baguette_bi.charts.altair.preprocess import gather_requests, preprocess

VEGALITE_VERSION = alt.schema.SCHEMA_VERSION.lstrip("v")
VEGA_VERSION = "5"
VEGAEMBED_VERSION = "6"


class DataTransformRenderer(alt.utils.display.HTMLRenderer):
    def transform_spec(self, spec: dict) -> dict:
        chart = preprocess(alt.Chart.from_dict(spec))
        requests = gather_requests(chart)
        with ThreadPoolExecutor(10) as executor:
            futures = executor.map(lambda r: (r.id, r.execute()), requests)
            dataframes = {k: v for k, v in futures}
        if chart.datasets == alt.Undefined:
            chart.datasets = {}
        chart.datasets.update(
            {k: v.to_dict(orient="records") for k, v in dataframes.items()}
        )
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
