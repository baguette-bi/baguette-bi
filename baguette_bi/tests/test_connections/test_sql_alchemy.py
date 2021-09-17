import pandas as pd

from baguette_bi.connections.sql_alchemy import SQLAlchemyConnection
from baguette_bi.data_request import DataRequest


def test_execute(engine):
    df = pd.DataFrame({"x": range(10), "y": range(10)})
    df.to_sql("test", engine, index=False)
    conn = SQLAlchemyConnection(
        driver="postgresql",
        username="test",
        password="test",
        host="localhost",
        port=5432,
        database="test",
    )
    assert conn.execute(DataRequest(query="test")).equals(df)
