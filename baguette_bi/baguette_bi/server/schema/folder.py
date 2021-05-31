from typing import List

from baguette_bi.schema.base import Base
from baguette_bi.server.schema.chart import ChartList


class BaseFolder(Base):
    id: str
    name: str


class FolderList(BaseFolder):
    pass


class FolderRead(BaseFolder):
    children: List[FolderList]
    charts: List[ChartList]
