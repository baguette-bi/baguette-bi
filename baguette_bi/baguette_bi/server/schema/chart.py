from baguette_bi.schema.base import Base


class BaseChart(Base):
    id: str
    name: str


class ChartList(BaseChart):
    pass


class ChartRead(BaseChart):
    """TODO: parameters: Optional[Dict[str, Parameter]]"""
