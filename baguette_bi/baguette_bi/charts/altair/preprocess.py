from typing import Optional, Union

import altair as alt

from baguette_bi.charts.altair.utils import (
    iterchannels,
    itermulti,
    iterspecs,
    multi_charts,
    multi_items,
    prepend_transforms,
    unit_charts,
)
from baguette_bi.dataset import Dataset


class NotSupportedError(Exception):
    """When Altair feature is not supported yet"""


def aggregate_from_channel(channel) -> alt.AggregatedFieldDef:
    """Given an encoding channel with inline aggregation, return a corresponding
    altair.AggregatedFieldDef.
    """
    if channel.field == alt.Undefined:  # basically, count(), no field
        # channel, which didn't have a field before, gets one
        channel.field = "Count of Records"
        # and aggregate doesn't need a field
        return alt.AggregatedFieldDef.from_dict(
            {
                "op": channel.aggregate.to_dict(),
                "as": channel.field,
            }
        )
    # normal case, just aggregate a field
    agg_name = channel.aggregate.to_dict().capitalize()
    alias = "{} of {}".format(agg_name, channel.field.to_dict())
    return alt.AggregatedFieldDef.from_dict(
        {
            "op": channel.aggregate.to_dict(),
            "field": channel.field.to_dict(),
            "as": alias,
        }
    )


def _bin_names(field: alt.FieldName):
    field = field.to_dict()
    return f"{field}_bin_start", f"{field}_bin_end"


def bin_from_channel(channel) -> Optional[alt.BinTransform]:
    """Given a channel with inline bin transform, return a corresponding BinTransform.
    Returns None if binned is True.
    """
    if channel.bin.binned is True:
        return None
    field = channel.field.to_dict()
    aliases = _bin_names(field)
    return alt.BinTransform(bin=channel.bin, field=field, **{"as": aliases})


def update_binned_channels(encoding):
    encoding = encoding.copy()
    new_channels = {}
    for channel in iterchannels(encoding):
        if channel.bin != alt.Undefined and channel.bin.binned is not True:
            start, end = _bin_names(channel.field)
            b = channel.bin
            field = channel.field
            channel.field = alt.FieldName(start)
            # update axis title
            if isinstance(channel, (alt.X, alt.Y, alt.Row, alt.Column)):
                axis_title = f"{field} (binned)"
                if (
                    channel.axis != alt.Undefined
                    and channel.axis.title == alt.Undefined
                ):
                    channel.axis.title = axis_title
                elif channel.axis == alt.Undefined:
                    channel.axis = alt.Axis(title=axis_title)
    return encoding


def extract_inline_transforms_chart(chart: Union[alt.Chart, alt.UnitSpec]):
    """Given a lowest-level non-composite chart, return a new chart with inline
    transforms replaced with explicit ones.
    """
    if not isinstance(chart, unit_charts):
        raise TypeError(
            f"altair.Chart or altair.UnitSpec expected, got {chart.__class__.__name__}"
        )
    groupby = []
    aggregate = {}  # a dict to prevent duplicates
    for channel in iterchannels(chart.encoding):
        if channel.aggregate != alt.Undefined:
            agg_def = aggregate_from_channel(channel)
            alias = agg_def.to_dict()["as"]
            aggregate[alias] = agg_def
            channel.aggregate = alt.Undefined
            channel.field = alias
        elif channel.bin != alt.Undefined:
            raise NotImplementedError(
                "Server-side bin transforms are not supported yet"
            )
        else:
            groupby.append(channel.field.to_dict())
    if len(aggregate) > 0:
        agg_transform = alt.AggregateTransform(
            groupby=groupby, aggregate=[agg for _, agg in aggregate.items()]
        )
        if chart.transform == alt.Undefined:
            chart.transform = [agg_transform]
        else:
            chart.transform.append(agg_transform)
    return chart


def extract_inline_transforms_multi(chart):
    """Given an multiview Altair chart, return another one with inline transforms
    turned explicit.
    """
    for item in itermulti(chart):
        extract_inline_transforms(item)
    return chart


def extract_inline_transforms(chart):
    if isinstance(chart, unit_charts):
        return extract_inline_transforms_chart(chart)
    elif isinstance(chart, multi_charts):
        return extract_inline_transforms_multi(chart)
    raise TypeError(f"Unsupported chart class: {chart.__class__.__name__}")


AltairChartType = Union[
    alt.Chart, alt.LayerChart, alt.ConcatChart, alt.HConcatChart, alt.VConcatChart
]


def resolve_data_references(
    chart, data: Optional[alt.NamedData] = None, transforms: Optional[list] = None
):
    """Move altair.NamedData data to the actual chart unit specs."""
    if isinstance(chart, alt.Chart):
        return chart

    if transforms is not None:  # copy just in case
        transforms = [t.copy() for t in transforms]

    if isinstance(chart, multi_charts):
        if isinstance(chart.data, alt.NamedData):
            data = chart.data
        if transforms is not None:
            chart = prepend_transforms(chart, transforms)
            transforms = chart.transform
        elif chart.transform != alt.Undefined:
            transforms = chart.transform
        items = multi_items(chart)
        setattr(
            chart,
            items,
            [
                resolve_data_references(unit, data, transforms)
                for unit in itermulti(chart)
            ],
        )
        return chart

    if isinstance(chart, unit_charts):
        if data is not None:
            chart.data = data.copy()
        if transforms is not None:
            chart = prepend_transforms(chart, transforms)
        return chart


def preprocess(chart: AltairChartType) -> AltairChartType:
    """Given an Altair Chart, return a new chart with all inline transforms extracted."""
    chart = extract_inline_transforms(chart)
    return resolve_data_references(chart)


def gather_requests(chart) -> list:
    """Given a chart, look at each spec that has a NamedData and build a DataRequest
    suitable for execution. Replace data name with request.id, remove transforms.
    """
    requests = set()
    for spec in iterspecs(chart):
        if isinstance(spec.data, alt.NamedData) and spec.data.name in Dataset.registry:
            dataset = Dataset.registry.get(spec.data.name)
            transforms = spec.transform if spec.transform != alt.Undefined else None
            request = dataset.request(parameters=None, transforms=transforms)
            requests.add(request)
            spec.data.name = request.id
            spec.transform = alt.Undefined
    return requests
