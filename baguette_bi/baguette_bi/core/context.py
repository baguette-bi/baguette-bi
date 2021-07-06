import inspect
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, Optional

from pydantic import create_model

from baguette_bi.core.dataset import DatasetMeta


class RenderContext:
    def __init__(self, parameters: Optional[Dict[str, Any]] = None):
        self.parameters = parameters if parameters is not None else {}

    def execute(self, fn: Callable):
        """Execute a function in this context.

        Context parameters will be passed by name and converted according to the
        callable's arguments' type annotations, any Dataset dependencies will be
        resolved.
        """
        datasets = {}
        parameters = {}
        for name, par in inspect.signature(fn).parameters.items():
            if isinstance(par.default, DatasetMeta):
                datasets[name] = par.default()
            else:
                parameters[name] = (
                    par.annotation if par.annotation != inspect._empty else str,
                    ... if par.default == inspect._empty else par.default,
                )
        with ThreadPoolExecutor() as executor:
            futures = [
                (k, executor.submit(v.get_data, self)) for k, v in datasets.items()
            ]
            dfs = {k: v.result() for k, v in futures}
        model = create_model("TempModel", **parameters).parse_obj(self.parameters)
        return fn(**model.dict(), **dfs)
