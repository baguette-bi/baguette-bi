from typing import List, Optional, Tuple, Union

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


class BaseMixin:
    """Just a base class"""

    _registry = set()

    def __init_subclass__(cls):
        if hasattr(cls, "_inject"):
            cls._registry.add(cls)


class TopLevelMixin(BaseMixin):
    _inject = (alt.TopLevelMixin,)

    def preprocess(self):
        self._preprocess()
        return resolve_data_references(self)


class ChartMixin(BaseMixin):
    """All charts"""

    def _preprocess(self):
        raise NotImplementedError


class ItemsMixin(ChartMixin):
    """Charts with embedded items: layer, concat, hconcat, vconcat"""

    _type: str

    def _iteritems(self):
        yield from getattr(self, self._type)

    def _preprocess(self):
        yield from (i.preprocess() for i in self._iteritems())


class LayerMixin(ItemsMixin):
    _type = "layer"
    _inject = (alt.LayerChart, alt.LayerSpec)


class ConcatMixin(ItemsMixin):
    _type = "concat"
    _inject = (alt.ConcatChart, alt.NormalizedConcatSpecGenericSpec)


class HConcatMixin(ItemsMixin):
    _type = "hconcat"
    _inject = (alt.HConcatChart, alt.NormalizedHConcatSpecGenericSpec)


class VConcatMixin(ItemsMixin):
    _type = "vconcat"
    _inject = (alt.VConcatChart, alt.NormalizedVConcatSpecGenericSpec)


class FacetMixin(ChartMixin):
    _inject = (alt.FacetChart, alt.NormalizedFacetSpec)


class RepeatMixin(ChartMixin):
    _inject = (alt.RepeatChart, alt.RepeatSpec)


class SpecMixin(BaseMixin):
    """For working with elementary chart specs, something that has encodings inside,
    not other charts.
    """

    _inject = (
        alt.Chart,
        alt.UnitSpec,
        alt.FacetedUnitSpec,
        alt.UnitSpecWithFrame,  # in top-level facet charts
    )  # yes, they do not have a common ancestor

    def _preprocess(self):
        bin_ = self.encoding._extract_bin_transforms()
        aggregate = self.encoding._extract_aggregate_transform()
        transforms = []
        if len(bin_) > 0:
            transforms.extend(bin_)
        if aggregate is not None:
            transforms.append(aggregate)
        if len(transforms) > 0:
            self._extend_transforms(transforms)

    def _extend_transforms(self, transforms: List[alt.Transform]):
        if self.transform == alt.Undefined:
            self.transform = transforms
        else:
            self.transform.extend(transforms)


class EncodingMixin(BaseMixin):
    """For working with encodings: extract aggregates etc. Encoding, FacetedEncoding"""

    _inject = (alt.Encoding, alt.FacetedEncoding)

    def _iterchannels(self):
        for _, channel in self._iterchannels_with_name():
            yield channel

    def _iterchannels_with_name(self):
        for channel in self.to_dict():
            yield channel, getattr(self, channel)

    def _extract_inline_transforms(self) -> List[alt.Transform]:
        raise NotImplementedError

    def _extract_aggregate_transform(self) -> alt.AggregateTransform:
        """There is exactly one aggregate transform that can be extracted
        from an encoding.
        """
        groupby = []
        aggregate = []
        for channel in self._iterchannels():
            if channel.aggregate == alt.Undefined:
                groupby.append(channel.field)
            else:
                aggregate.append(channel._extract_aggregate_field())
        if len(aggregate) > 0:
            return alt.AggregateTransform(groupby=groupby, aggregate=aggregate)

    def _extract_bin_transforms(self) -> List[alt.BinTransform]:
        """There can be multiple bin transforms in a given encoding. Also, encoding
        itself might have to be injected with additional channels."""
        transforms = []
        for name, channel in self._iterchannels_with_name():
            transform = channel._extract_bin_transform()
            # add x2, y2 channel if needed
            if (
                transform is not None
                and isinstance(channel, alt.PositionFieldDef)
                and channel.type == "quantitative"
            ):
                channel2 = alt.PositionFieldDef(
                    field=transform["as"][1], type="quantitative"
                )
                setattr(self, f"{name}2", channel2)
            if transform is not None:
                transforms.append(transform)
        return transforms


def _bin_names(field: alt.FieldName) -> Tuple[str, str]:
    field = field.to_dict()
    return alt.FieldName(f"{field}_bin_start"), alt.FieldName(f"{field}_bin_end")


def _merge_default(obj, default):
    for key, attr in default.__dict__.items():
        if getattr(obj, key) == alt.Undefined:
            setattr(obj, key, attr)
        else:
            _merge_default(getattr(obj, key), attr)


class ChannelMixin(BaseMixin):
    """Methods for working with individual encoding channels."""

    # _inject = (
    #     alt.PositionFieldDef,  # x, y
    #     alt.ColorGradientFieldDefWithCondition,  # color channel
    #     alt.RowColumnEncodingFieldDef,
    # )

    def _extract_aggregate_field(self) -> alt.AggregatedFieldDef:
        """Get AggregatedFieldDef, replace field name with aggregated field name"""
        aggregate_field = self.field
        alias = alt.FieldName("Count of Records")
        if self.field != alt.Undefined:
            agg_name = self.aggregate.to_dict().capitalize()
            alias = "{} of {}".format(agg_name, self.field.to_dict())
        alias = alt.FieldName(alias)
        aggregate = self.aggregate
        self.aggregate = alt.Undefined
        self.field = alias
        return alt.AggregatedFieldDef(
            op=aggregate, field=aggregate_field, **{"as": alias}
        )

    def _extract_bin_transform(self) -> alt.BinTransform:
        """Bin transform is extracted per channel."""
        if self.bin == alt.Undefined or self.bin.binned is True:
            return None
        bin_ = self.bin
        self.bin = alt.Undefined
        aliases = _bin_names(self.field)
        transform = alt.BinTransform(bin=bin_, field=self.field, **{"as": aliases})
        self._tranform_prebinned(transform)
        return transform

    def _merge_default(self, encoding):
        """Merge self with given encoding defaults. Field and type are set as in the
        given encoding, other attributes are only set if Undefined in self, recursively
        for all nested attributes.
        """
        for key, attr in encoding.__dict__.items():
            if key == "field":
                self.field = attr
            elif key == "type":
                self.type = attr
            elif getattr(self, key) == alt.Undefined:
                setattr(self, key, attr)
            else:
                _merge_default(getattr(self, key), attr)

    def _tranform_prebinned(self, transform: alt.BinTransform):
        """Transform self to receive prebinned data. Implemented for each channel
        type separately.
        """
        raise NotImplementedError


class PositionChannelMixin(ChannelMixin):
    _inject = (alt.PositionFieldDef,)  # x, y

    def _tranform_prebinned(self, transform: alt.BinTransform):
        self.bin = (
            alt.Bin(binned=True) if self.type == "quantitative" else alt.Undefined
        )
        self.field = getattr(transform, "as")[0]


class ColorChannelMixin(ChannelMixin):
    _inject = (alt.ColorGradientFieldDefWithCondition,)  # color, fill, stroke

    def _tranform_prebinned(self, transform: alt.BinTransform):
        self.bin = alt.Undefined
        self.field = getattr(transform, "as")[0]


class NumericChannelMixin(ChannelMixin):
    _inject = (alt.NumericFieldDefWithCondition,)  # opacity, size etc.

    def _tranform_prebinned(self, transform: alt.BinTransform):
        self.bin = alt.Undefined
        self.field = getattr(transform, "as")[0]


def monkeypatch_altair():
    for cls in BaseMixin._registry:
        for altair_cls in cls._inject:
            if cls not in altair_cls.__bases__:
                altair_cls.__bases__ += (cls,)


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


def bin_from_channel(channel) -> Optional[alt.BinTransform]:
    """Given a channel with inline bin transform, return a corresponding BinTransform.
    Returns None if binned is True.
    """
    if channel.bin.binned is True:
        return None
    aliases = _bin_names(channel.field)
    return alt.BinTransform(bin=channel.bin, field=channel.field, **{"as": aliases})


def binned_axis_quantitative(field: str):
    f0, f1 = _bin_names(field)
    return alt.FacetedEncoding(
        x=alt.X(
            field=alt.FieldName(f0),
            type="quantitative",
            bin=alt.BinParams(binned=True),
            axis=alt.Axis(title=f"{field} (binned)"),
        ),
        x2=alt.X2(field=alt.FieldName(f1), type="quantitative"),
    )


def binned_axis_ordinal_nominal(field: str, type_: str):
    f0, f1 = _bin_names(field)
    return alt.FacetedEncoding(
        x=alt.X(
            field=alt.FieldName(f"{f0}_{f1}_range"),
            type=type_,
            axis=alt.Axis(title=f"{field} (binned)"),
        )
    )


def binned_color(field: str):
    f0, _ = _bin_names(field)
    return alt.FacetedEncoding(
        color=alt.Color(
            field=alt.FieldName(f0),
            type="ordinal",
            scale=alt.Scale(type=alt.ScaleType("bin-ordinal")),
            legend=alt.Legend(title=f"{field} (binned)"),
        )
    )


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
        elif channel.bin != alt.Undefined and channel.bin.binned is not True:
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
