import json
from functools import cached_property
from hashlib import md5


class IDMixin:
    """Generates an object ID based on provided unique details"""

    @cached_property
    def id(self):
        details = self.details()
        return md5(json.dumps(details, sort_keys=True).encode()).hexdigest()

    def details(self) -> dict:
        raise NotImplementedError
