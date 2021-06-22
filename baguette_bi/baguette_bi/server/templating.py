import inspect
from pathlib import Path
from typing import Dict
from urllib.parse import urlencode, urljoin

from babel import dates, numbers
from jinja2 import Environment, FileSystemLoader, pass_context
from jinja2.runtime import Macro

from baguette_bi.server import project, settings, templates

inner = Environment(loader=FileSystemLoader(templates.path))
pages = Environment(
    loader=FileSystemLoader(Path(settings.project).resolve() / settings.pages_dir)
)


def DataFrame(path: str):
    return project.get_project().datasets.get(path).get_data()


def _fmt(round: int, sep: bool):
    whl = ",###" if sep else "#"
    dec = "#" * round
    return whl, dec


def format_percent(
    val,
    round: int = 0,
    thousands_separator: bool = True,
    locale=settings.locale,
    default="N/A",
):
    if val is None:
        return default
    whl, dec = _fmt(round, thousands_separator)
    fmt = f"{whl}.{dec}%"
    return numbers.format_percent(val, format=fmt, locale=locale)


def format_number(
    val,
    round=0,
    format=None,
    thousands_separator=True,
    locale=settings.locale,
    default="N/A",
):
    if val is None:
        return default
    whl, dec = _fmt(round, thousands_separator)
    fmt = f"{whl}.{dec}" if format is None else format
    return numbers.format_decimal(val, format=fmt, locale=locale)


def format_currency(
    val, currency="USD", currency_digits=True, locale=settings.locale, default="N/A"
):
    if val is None:
        return default
    return numbers.format_currency(
        val,
        currency=currency,
        currency_digits=currency_digits,
        locale=locale,
    )


def format_date(val, format="medium", locale=settings.locale, default="N/A"):
    if val is None:
        return default
    return dates.format_date(val, format=format, locale=locale)


@pass_context
def text_strong(context, *args, **kwargs):
    return context["strong_inline"](*args, **kwargs)


@pass_context
def text_em(context, *args, **kwargs):
    return context["em_inline"](*args, **kwargs)


@pass_context
def text_underline(context, *args, **kwargs):
    return context["underline_inline"](*args, **kwargs)


@pass_context
def text_strike(context, *args, **kwargs):
    return context["strike_inline"](*args, **kwargs)


@pass_context
def text_mark(context, *args, **kwargs):
    return context["mark_inline"](*args, **kwargs)


@pass_context
def text_big(context, *args, **kwargs):
    return context["big_inline"](*args, **kwargs)


@pass_context
def text_small(context, *args, **kwargs):
    return context["small_inline"](*args, **kwargs)


@pass_context
def text_muted(context, *args, **kwargs):
    return context["muted_inline"](*args, **kwargs)


@pass_context
def text_paren(context, *args, **kwargs):
    return context["wrap_in_paren"](*args, **kwargs)


pages.filters["format_percent"] = format_percent
pages.filters["fpct"] = format_percent

pages.filters["format_number"] = format_number
pages.filters["fnum"] = format_number

pages.filters["format_currency"] = format_currency
pages.filters["fcur"] = format_currency

pages.filters["format_date"] = format_date
pages.filters["fdate"] = format_date

pages.filters["strong"] = text_strong
pages.filters["em"] = text_em
pages.filters["underline"] = text_underline
pages.filters["strike"] = text_strike
pages.filters["big"] = text_big
pages.filters["small"] = text_small
pages.filters["muted"] = text_muted
pages.filters["mark"] = text_mark
pages.filters["paren"] = text_paren


pages_macros = inner.get_template("pages_macros.html.j2")
for name, m in inspect.getmembers(pages_macros.module, lambda m: isinstance(m, Macro)):
    pages.globals[name] = m


def pages_url(path: str, params: Dict = None):
    abspath = urljoin("/pages/", path)
    _params = params if params is not None else {}
    qs = urlencode(_params)
    if qs:
        qs = f"?{qs}"
    return f"{abspath}{qs}"


def link(text: str, path: str, **params):
    url = pages_url(path, params)
    return pages_macros.module.mklink(url, text)


pages.filters["link"] = link


def table(df, **kwargs):
    return pages_macros.module.mktable(df, **kwargs)


def big_number(*args, **kwargs):
    return pages_macros.module.mk_big_number(*args, **kwargs)


pages.filters["table"] = table
pages.filters["big_number"] = big_number
