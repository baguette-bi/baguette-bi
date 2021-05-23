import json
from hashlib import md5


class Folder:
    def __init__(self, name, parent: "Folder" = None):
        self.name = name
        self.children = []
        self.charts = []
        self.parent = parent
        if parent is not None:
            parent.children.append(self)
        self.id = md5(json.dumps(self.dict()).encode("UTF-8")).hexdigest()

    def dict(self):
        return {
            "name": self.name,
            "parent": None if self.parent is None else self.parent.dict(),
        }

    def __hash__(self) -> int:
        return hash(id(self))
