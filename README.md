# Baguette BI

Baguette BI is a  Business Intelligence web framework. It is made for teams who love code and care about version control, testing and reproducibility.

Baguette is made to solve a particular set of problems very common within BI teams. They usually involve some version of this scenario: "someone changed something and now everything is broken". This is strange, because this isn't a problem in "normal" software engineering. Programmers test their code and are able to catch such problems before they reach the production environment.

Baguette BI is currently in development and things will probably change quickly. Right now it's very minimal and allows you to do one thing: describe how your data visualizations/dashboards are to be constructed from datasets with code and run a web server on top of this description.

# Quick example

So how does a minimal example look?

A chart is a Python class. You define various class attributes (e.g. name, folder where the chart should be displayed etc.) and a `render` method that must return an instance of supported chart class (currently only Altair is supported).

```py
import altair as alt
from baguette_bi import bi
from pandas import DataFrame

# a connection describes a place you can get data from:
# a database, an API, Google Cloud service account
# (for reading Google Spreadsheets), etc.
vega = bi.VegaDatasetsConnection()

# a dataset describes how to get data from the connection
# it has a name (used for displaying it in the web interface)
# and a query (an arbitrary value that depends on the type of connection)
# for SQL-based connection it will be an SQL query,
# for MongoDB a query dict, for VegaDatasetsConnection it's just a name of the dataset
movies = vega.dataset(name="Movies", query="movies")
my_folder = bi.Folder(name="MyFolder)

class MoviesChart(bi.AltairChart):
    name = "My First Altair Chart"  # you can skip this and Baguette will generate a nice-looking name from the class name
    folder = my_folder

    # render method can "request" different resources,
    # namely datasets and parameters. Baguette will make sure
    # that they will be passed to the method when it is called
    # if you specify a dataset as a default for an argument, the resulting
    # Pandas DataFrame will be passed to the function. Argument name and
    # type annotation don't matter — only the default value.
    def render(self, df: DataFrame = movies):
        return (
            alt.Chart(df)
            .mark_rect()
            .encode(
                alt.X("IMDB_Rating:Q", bin=alt.Bin(maxbins=60)),
                alt.Y("Rotten_Tomatoes_Rating:Q", bin=alt.Bin(maxbins=40)),
                alt.Color("count(IMDB_Rating):Q", scale=alt.Scale(scheme="greenblue")),
            )
        )
```

If baguette package is installed, you can run this file with `baguette server example.py`. Then go to `localhost:8000`, and you should see a folder with a chart in it.

# Roadmap

These things are not implemented yet, but will be in the future (in rough order of importance):

- Chart previews in the web interface
- Docs beyond a meager README file
- Parametrization of charts and datasets
- Correct locale handling for Altair
- Dashboards (layouts of many charts) as first-class citizens
- Support of other libraries (Bokeh, etc.)

# Release notes

## 0.1.3

- Authentication and user permissions
- this README
- bi.test for rendering charts in Jupyter
