import altair as alt

from baguette_bi import actions
from baguette_bi.server.project import project


def test_test():
    chart = project.root.children[0].charts[0]
    assert isinstance(actions.test(chart), alt.Chart)
