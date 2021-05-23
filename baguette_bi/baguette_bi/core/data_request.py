from typing import Dict, Any, Optional


class DataTransform:
    pass


class DataRequest:
    def __init__(self, query: str, parameters: Optional[Dict[str, Any]] = None):
        self.query = query
        self.parameters = parameters if parameters is not None else {}
