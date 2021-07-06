from pathlib import Path

from baguette_bi.server import static


def print_ascii():
    import locale

    from baguette_bi import __version__

    loc, _ = locale.getlocale()
    logo = "baguette_moscow.txt" if loc == "ru_RU" else "baguette.txt"
    path = Path(static.__file__).parent / logo
    print(path.read_text().replace("__version__", __version__))


def run():
    print_ascii()
