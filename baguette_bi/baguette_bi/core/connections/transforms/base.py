from typing import Any, Dict


class BaseTransformMixin:
    def transform_aggregate(self, prev: Any, spec: Dict):
        raise NotImplementedError

    def transform_filter(self, prev: Any, spec: Dict):
        raise NotImplementedError

    def transform_calculate(self, prev: Any, spec: Dict):
        raise NotImplementedError

    def transform_sample(self, prev: Any, spec: Dict):
        raise NotImplementedError
