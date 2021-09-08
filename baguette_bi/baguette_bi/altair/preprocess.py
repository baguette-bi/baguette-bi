from typing import List, Tuple

import altair as alt

from baguette_bi.utils import Empty, NamespaceDict


class NotSupportedError(Exception):
    """When Altair feature is not supported yet"""


types = ["concat", "vconcat", "hconcat", "layer", "repeat", "facet"]
multiview_charts = types[:4]


class Chart(NamespaceDict):
    @property
    def type(self):
        for t in types:
            if self.t != Empty:
                return t
        return "chart"

    @property
    def items(self):
        if self.type in multiview_charts:
            return self[self.type]

    @items.setter
    def items(self, vals: List):
        if self.items is None:
            raise TypeError("Chart is not compound")
        self[self.type] = vals


def iterchannels(encoding: alt.FacetedEncoding):
    for channel_name in encoding.to_dict():
        yield getattr(encoding, channel_name)


def extract_aggregate(encoding) -> Tuple:
    """Given view encoding, return extracted explicit AggregateTransform and a new
    encoding without inline transforms.
    If there are no aggregations, return (None, None)
    """
    groupby = []
    aggregate = []
    encoding = encoding.copy()
    for channel in iterchannels(encoding):
        if channel.aggregate != alt.Undefined:
            if channel.field == alt.Undefined:  # basically, count()
                aggregate.append(  # in this case, aggregate doesn't need a field
                    alt.AggregatedFieldDef.from_dict(
                        {
                            "op": channel.aggregate.to_dict(),
                            "as": channel.aggregate.to_dict(),
                        }
                    )
                )
                # and channel, which didn't have a field before, gets one
                channel.field = channel.aggregate.to_dict()
            else:  # normal case, just aggregate
                aggregate.append(
                    alt.AggregatedFieldDef.from_dict(
                        {
                            "op": channel.aggregate.to_dict(),
                            "field": channel.field.to_dict(),
                            "as": channel.field.to_dict(),
                        }
                    )
                )
            channel.aggregate = alt.Undefined
        else:
            groupby.append(channel.field.to_dict())
    if len(aggregate) > 0:
        transform = alt.AggregateTransform(
            groupby=groupby,
            aggregate=aggregate,
        )
        return transform, encoding
    return None, None


def extract_inline_transforms_facet(obj):  # pragma: no cover
    # TODO: support
    raise NotSupportedError("Facet charts are not supported yet")
    transform, encoding = extract_aggregate(obj.spec.encoding)
    if obj.transform is Empty:
        obj.transform = []
    if obj.spec.transform is not Empty:
        obj.transform.extend(obj.spec.transform)
        obj.spec.transform = Empty
    obj.transform.append(transform)
    obj.spec.encoding = encoding


def extract_inline_transforms_repeat(obj):  # pragma: no cover
    # TODO: support
    raise NotSupportedError("Repeat Charts are not supported yet")


def extract_inline_transforms(chart) -> dict:
    """Recursively go through embedded view definitions and turn inline transforms
    into explicit ones. Returns a resulting spec dict.
    """
    # TODO: drunk, use altair class
    # if chart.items is not None:
    #     chart.items = [extract_inline_transforms(i) for i in chart.items]
    # elif chart.type == "facet":
    #     extract_inline_transforms_facet(chart)
    # elif chart.type == "repeat":
    #     extract_inline_transforms_repeat(chart)
    if isinstance(chart, alt.Chart):
        transform_aggregate, encoding = extract_aggregate(chart.encoding)
        if transform_aggregate is not None:
            if chart.transform == alt.Undefined:
                chart.transform = [transform_aggregate]
            else:
                chart.transform.append(transform_aggregate)
            chart.encoding = encoding
    else:
        raise NotImplementedError(
            f"Chart class {chart.__class__.__name__} is not yet supported"
        )
    return chart
