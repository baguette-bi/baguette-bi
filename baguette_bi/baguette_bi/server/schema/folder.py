from typing import List

from .base import Base
from .chart import ChartList


class BaseFolder(Base):
    id: str
    name: str


class FolderList(BaseFolder):
    pass


class FolderRead(BaseFolder):
    children: List[FolderList]
    charts: List[ChartList]
