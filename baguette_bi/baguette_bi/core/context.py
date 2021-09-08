import inspect
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, Optional

import pandas as pd
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
        parameters = self.resolve_parameters(fn)
        dataframes = self.resolve_datasets(fn)
        return fn(**parameters, **dataframes)

    def resolve_parameters(self, fn: Callable) -> Dict:
        """Search current context for requested parameters, return a dict of those,
        converted to an appropriate type.
        """
        parameters = {}
        for name, par in inspect.signature(fn).parameters.items():
            if not isinstance(par.default, DatasetMeta):
                parameters[name] = (
                    par.annotation if par.annotation != inspect._empty else str,
                    ... if par.default == inspect._empty else par.default,
                )
        model = create_model("TempModel", **parameters).parse_obj(self.parameters)
        return model.dict()

    def resolve_datasets(self, fn: Callable) -> Dict[str, pd.DataFrame]:
        """Search function signature for arguments that have a Dataset as their default.
        Execute dataset in current context and return a dict containing dataframes.
        """
        datasets = {}
        for name, par in inspect.signature(fn).parameters.items():
            if isinstance(par.default, DatasetMeta):
                datasets[name] = par.default()
        with ThreadPoolExecutor() as executor:
            futures = [
                (k, executor.submit(v.get_data, self)) for k, v in datasets.items()
            ]
            return {k: v.result() for k, v in futures}
