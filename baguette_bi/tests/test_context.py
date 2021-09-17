from datetime import date
from time import sleep, time

from baguette_bi.dataset import Dataset
from baguette_bi.render_context import RenderContext


def test_convert_parameters():
    ctx = RenderContext(parameters={"a": "42", "b": "3.14", "dt": "2021-01-01"})

    def fn(a: int, b: float, dt: date, c: int = 12):
        return a, b, dt, c

    assert ctx.execute(fn) == (42, 3.14, date(2021, 1, 1), 12)


def test_datasets_parallel():
    ctx = RenderContext()

    class SlowDataset(Dataset):
        def get_data(self, ctx):
            sleep(1)
            return 2

    def fn(a=SlowDataset, b=SlowDataset):
        return a, b

    start = time()
    assert ctx.execute(fn) == (2, 2)
    assert time() - start < 1.1
