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

### 0.1.11
- Update dependencies

### 0.1.10
- fix bug in `set_params` that mutated template context

### 0.1.9
- Admins and developers can see Python stacktrace when there's a server error
- `set_params` filter for creating links manipulating parameter state on the same page


### 0.1.8
- fix incorrent login flow (too many redirects)

### 0.1.7
- sidebar
- chart error handling on the frontend
- redirect to requested page after successful login

### 0.1.6
- better handling of https static assets
- redis cache

### 0.1.5
- better default for development and production mode
- stdlib `date`, `datetime` and `timedelta` are available in page templates

### 0.1.4
- Fix bug that broke authentication

### 0.1.3

- Authentication and user permissions
- this README
- bi.test for rendering charts in Jupyter
