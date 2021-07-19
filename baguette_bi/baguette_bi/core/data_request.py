import json
from hashlib import md5
from typing import Any, Dict, Optional


class DataTransform:
    pass


class DataRequest:
    def __init__(self, query: str, parameters: Optional[Dict[str, Any]] = None):
        self.query = query
        self.parameters = parameters if parameters is not None else {}
        self.id = md5(
            json.dumps(self.dict(), sort_keys=True, default=str).encode()
        ).hexdigest()

    def dict(self):
        return {"query": self.query, "parameters": self.parameters}
