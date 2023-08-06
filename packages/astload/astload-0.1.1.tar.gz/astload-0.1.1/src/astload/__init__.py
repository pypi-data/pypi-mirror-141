"""ASTLoad - Create ASTs from `ast.dump()` output."""
import ast

_AST_VARS = {key: val for key, val in vars(ast).items() if not key.startswith("_")}


def load(ast_string: str) -> ast.AST:
    return eval(ast_string, _AST_VARS.copy())


def install() -> None:
    ast.load = load
