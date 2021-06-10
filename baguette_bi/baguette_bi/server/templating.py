import inspect
from pathlib import Path
from urllib.parse import urlencode, urljoin

from babel import dates, numbers
from jinja2 import Environment, FileSystemLoader, pass_context
from jinja2.runtime import Macro

from baguette_bi.server import project, settings, templates

inner = Environment(loader=FileSystemLoader(Path(templates.__file__).parent.resolve()))
pages = Environment(
    loader=FileSystemLoader(Path(settings.project).resolve() / settings.pages_dir)
)


def make_pages_link(path, params=None):
    abspath = urljoin("/pages/", path)
    _params = params if params is not None else {}
    qs = urlencode(_params)
    return f"{abspath}?{qs}"


def DataFrame(path: str):
    return project.get_project().datasets.get(path).get_data()


def _fmt(round: int, sep: bool):
    whl = ",###" if sep else "#"
    dec = "#" * round
    return whl, dec


def format_percent(num, round: int = 0, thousands_separator: bool = True):
    whl, dec = _fmt(round, thousands_separator)
    fmt = f"{whl}.{dec}%"
    return numbers.format_percent(num, format=fmt, locale=settings.locale)


def format_number(num, round=0, thousands_separator=True):
    whl, dec = _fmt(round, thousands_separator)
    fmt = f"{whl}.{dec}"
    return numbers.format_decimal(num, format=fmt, locale=settings.locale)


def format_date(dt, format="medium"):
    return dates.format_date(dt, format=format, locale=settings.locale)


@pass_context
def text_strong(context, *args, **kwargs):
    return context["strong_inline"](*args, **kwargs)


@pass_context
def text_big(context, *args, **kwargs):
    return context["big_inline"](*args, **kwargs)


@pass_context
def text_small(context, *args, **kwargs):
    return context["small_inline"](*args, **kwargs)


@pass_context
def text_small_muted(context, *args, **kwargs):
    return context["small_muted_inline"](*args, **kwargs)


@pass_context
def text_paren(context, *args, **kwargs):
    return context["wrap_in_paren"](*args, **kwargs)


pages.filters["format_percent"] = format_percent
pages.filters["fpct"] = format_percent

pages.filters["format_number"] = format_number
pages.filters["fnum"] = format_number

pages.filters["format_date"] = format_date
pages.filters["fdate"] = format_date

pages.filters["strong"] = text_strong
pages.filters["big"] = text_big
pages.filters["small"] = text_small
pages.filters["small_muted"] = text_small_muted
pages.filters["paren"] = text_paren


inner.filters["make_pages_link"] = make_pages_link

pages_macros = inner.get_template("pages_macros.html.j2")
for name, m in inspect.getmembers(pages_macros.module, lambda m: isinstance(m, Macro)):
    pages.globals[name] = m
