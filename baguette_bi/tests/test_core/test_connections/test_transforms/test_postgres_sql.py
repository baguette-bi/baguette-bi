from baguette_bi.core.connections.transforms.standard_sql import (
    StandardSQLTransformMixin,
)


def test_aggregate():
    transform = {
        "groupby": ["gb1", "gb2"],
        "aggregate": [
            {"op": "sum", "field": "x", "as": "y"},
            {"op": "mean", "field": "a", "as": "b"},
        ],
    }
    prev = "select * from tbl"
    result = (
        "select gb1, gb2, sum(x) as y, avg(a) as b "
        "from (select * from tbl) as t "
        "group by gb1, gb2"
    )
    assert StandardSQLTransformMixin().transform_aggregate(prev, transform) == result
