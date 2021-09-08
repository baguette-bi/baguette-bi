import json
from hashlib import md5
from typing import Any, Dict, List, Optional


class DataTransform:
    pass


class DataRequest:
    def __init__(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        transforms: Optional[List] = None,
        echo: bool = False,
    ):
        self.query = query
        self.parameters = parameters if parameters is not None else {}
        self.transforms = transforms if transforms is not None else []
        self.echo = echo
        self.id = md5(
            json.dumps(self.dict(), sort_keys=True, default=str).encode()
        ).hexdigest()

    def dict(self):
        return {
            "query": self.query,
            "parameters": self.parameters,
            "transforms": self.transforms,
        }
