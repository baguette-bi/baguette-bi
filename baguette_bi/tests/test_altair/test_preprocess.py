import altair as alt
import pytest

from baguette_bi.altair.preprocess import (
    Chart,
    NotSupportedError,
    extract_aggregate,
    extract_inline_transforms_chart,
    extract_inline_transforms_facet,
    extract_inline_transforms_repeat,
)


def test_extract_aggregate():
    ch = (
        alt.Chart("#")
        .mark_text()
        .encode(
            x="groupby_field:N",
            y="sum(agg_field):Q",
        )
    )
    ch = Chart(ch.to_dict())
    agg, encoding = extract_aggregate(ch.encoding)
    assert agg is not None
    assert agg.to_dict() == {
        "groupby": ["groupby_field"],
        "aggregate": [{"op": "sum", "field": "agg_field", "as": "agg_field"}],
    }
    assert encoding.to_dict() == {
        "x": {"field": "groupby_field", "type": "nominal"},
        "y": {"field": "agg_field", "type": "quantitative"},
    }


def test_extract_aggregate_multiple():
    ch = (
        alt.Chart("#")
        .mark_text()
        .encode(
            x="groupby_field:N",
            color="color_nom:N",
            y="sum(agg_field):Q",
            opacity="mean(opac):Q",
        )
    )
    ch = Chart(ch.to_dict())
    agg, encoding = extract_aggregate(ch.encoding)
    assert agg is not None
    assert set(agg.groupby) == {"groupby_field", "color_nom"}
    assert len(agg.aggregate) == 2
    assert encoding.to_dict() == {
        "x": {"field": "groupby_field", "type": "nominal"},
        "y": {"field": "agg_field", "type": "quantitative"},
        "color": {"field": "color_nom", "type": "nominal"},
        "opacity": {"field": "opac", "type": "quantitative"},
    }


def test_extract_inline_transforms_repeat():
    with pytest.raises(NotSupportedError):
        extract_inline_transforms_repeat(None)


def test_extract_inline_transforms_facet():
    with pytest.raises(NotSupportedError):
        extract_inline_transforms_facet(None)


def test_extract_inline_tranforms_chart():
    ch = (
        alt.Chart("#")
        .mark_text()
        .encode(
            x="groupby_field:N",
            y="sum(agg_field):Q",
        )
    )
    spec = extract_inline_transforms_chart(ch.to_dict())
    newch = Chart(spec)
    assert len(newch.transform) == 1
    assert newch.transform[0].to_dict() == {
        "groupby": ["groupby_field"],
        "aggregate": [{"field": "agg_field", "as": "agg_field", "op": "sum"}],
    }
