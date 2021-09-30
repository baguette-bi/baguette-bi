from lark import Token, Transformer, Tree, Visitor


def _is_string(x):
    """Check if an expression is a string."""
    if isinstance(x, Token):  # x is a STRING
        if x.type == "STRING":
            return True
    # x is a concat or toString call
    elif x.data == "concat" or x.data == "call" and x.children[0] == "toString":
        return True
    # x is a string inside paren (recurse)
    elif x.data == "paren" and _is_string(x.children[0]):
        return True
    return False


class ConcatVisitor(Visitor):
    """JS (and so Vega Expressions) don't distinguish between concatenation and addition
    and there's also implicit type casts (ugh). So for any addition, we need to determine
    if any of the operands are STRING, and if so, convert the other non-STRING ones to
    string with toString call and replace add with concat.
    """

    def add(self, tree: Tree):
        if any(_is_string(c) for c in tree.children):
            left, right = tree.children
            if not _is_string(left):
                left = Tree("call", ["toString", left])
            if not _is_string(right):
                right = Tree("call", ["toString", right])
            tree.data = "concat"
            tree.children = [left, right]


concat_visitor = ConcatVisitor()


class Compiler(Transformer):
    def compile(self, tree: Tree):
        return self.transform(concat_visitor.visit(tree))
