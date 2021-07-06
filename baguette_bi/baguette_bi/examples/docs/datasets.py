import pandas as pd
from vega_datasets import data

from baguette_bi import bi

vega = bi.VegaDatasetsConnection()


class Cars(bi.Dataset):
    connection = vega
    query = "cars"


class VegaDatasetsList(bi.Dataset):
    def get_data(self, render_context):
        return pd.DataFrame(data={"dataset": data.list_datasets()})


class AnyVegaDataset(bi.Dataset):
    connection = vega
    query = "{{ dataset_name }}"

    class Parameters:
        dataset_name: str
