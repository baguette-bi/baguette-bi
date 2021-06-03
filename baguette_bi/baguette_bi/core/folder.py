import json
from hashlib import md5
from typing import List

from baguette_bi.core.chart import Chart
from baguette_bi.core.permissions import Permissions


class Folder:
    def __init__(
        self,
        name,
        parent: "Folder" = None,
        permissions: str = Permissions.inherit,
    ):
        self.name = name
        self.children: List[Folder] = []
        self.charts: List[Chart] = []
        self.parent = parent
        self.permissions = permissions
        self.id = md5(json.dumps(self.dict()).encode("UTF-8")).hexdigest()

    def dict(self):
        return {
            "name": self.name,
            "parent": None if self.parent is None else self.parent.dict(),
        }

    def __hash__(self) -> int:
        return hash(id(self))
