from baguette_bi import bi

vega = bi.VegaDatasetsConnection()


class UsEmployment(bi.Dataset):
    connection = vega
    query = "us_employment"
