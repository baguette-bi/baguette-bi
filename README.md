# Baguette BI

Baguette BI is a  Business Intelligence web framework. It is made for teams who love code and care about version control, testing and reproducibility.


## Documentation

Baguette BI's Documentation is built with Baguette itself. You can run in by first
installing:

```sh
pip install baguette-bi
```

And then running this command:

```sh
baguette docs
```


## Roadmap

These things are not implemented yet, but will be in the future (in rough order of importance):

- Improved documentation
  - More structured and full reference
  - Server settings reference
  - A more advanced tutorial
- Caching with Redis
- User administration in the web interface (in addition to CLI)
- Support other libraries (Bokeh, etc.)


## Release notes

### 0.1.4
- Fix bug that broke authentication

### 0.1.3

- Authentication and user permissions
- this README
- bi.test for rendering charts in Jupyter
