from pathlib import Path

from lark import Lark

grammar = Path(__file__).parent / "expr.lark"
parser = Lark(grammar.read_text(), start="expr")
