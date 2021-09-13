import altair as alt


def iterchannels(encoding):
    for channel_name in encoding.to_dict():
        yield getattr(encoding, channel_name)


unit_charts = (alt.Chart, alt.UnitSpec, alt.FacetedUnitSpec)
layer_charts = (alt.LayerChart, alt.LayerSpec)
concat_charts = (
    alt.ConcatChart,
    alt.ConcatSpecGenericSpec,
    alt.NormalizedConcatSpecGenericSpec,
)
hconcat_charts = (
    alt.HConcatChart,
    alt.HConcatSpecGenericSpec,
    alt.NormalizedHConcatSpecGenericSpec,
)
vconcat_charts = (
    alt.VConcatChart,
    alt.VConcatSpecGenericSpec,
    alt.NormalizedVConcatSpecGenericSpec,
)
multi_charts = concat_charts + hconcat_charts + vconcat_charts + layer_charts


def iterspecs(chart):
    """Recursively iterate all specs in a chart"""
    if isinstance(chart, unit_charts):
        yield chart
    elif isinstance(chart, multi_charts):
        for item in itermulti(chart):
            yield from iterspecs(item)
    else:
        raise TypeError(f"Unsupported chart class {chart.__class__.__name__}")


def multi_items(chart) -> str:
    if isinstance(chart, layer_charts):
        return "layer"
    elif isinstance(chart, concat_charts):
        return "concat"
    elif isinstance(chart, hconcat_charts):
        return "hconcat"
    elif isinstance(chart, vconcat_charts):
        return "vconcat"
    else:
        raise TypeError(f"Unsupported chart class {chart.__class__.__name__}")


def itermulti(chart):
    """Iterate multichart items"""
    yield from getattr(chart, multi_items(chart))


def append_transforms(chart, transforms):
    if chart.transform == alt.Undefined:
        chart.transform = transforms
    else:
        chart.transform.extend(transforms)
    return chart


def prepend_transforms(chart, transforms):
    if chart.transform == alt.Undefined:
        chart.transform = transforms
    else:
        chart.transform[:0] = transforms
    return chart
