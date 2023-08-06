# astload

Create ASTs from `ast.dump()` output.

It's possible to serialize an AST node from Python's `ast` module to a string,
using `ast.dump`. However, it's not possible to convert the said string back to
an AST node. This simple module adds that functionality.

## Examples

We will take a simple Python AST, serialize it and then deserialize it:

```pycon
>>> import ast
>>> import astload
>>> tree1 = ast.parse('1 == 2')
>>> ast_string = ast.dump(tree1, indent=2)
>>> print(ast_string)
Module(
  body=[
    Expr(
      value=Compare(
        left=Constant(value=1),
        ops=[
          Eq()],
        comparators=[
          Constant(value=2)]))],
  type_ignores=[])
>>> tree2 = astload.load(ast_string)
>>> print(ast.dump(tree2, indent=2))
Module(
  body=[
    Expr(
      value=Compare(
        left=Constant(value=1),
        ops=[
          Eq()],
        comparators=[
          Constant(value=2)]))],
  type_ignores=[])
>>> ast.dump(tree1) == ast.dump(tree2)
True
>>> ast.unparse(tree2)
'1 == 2'
```

### Adding `load()` to the `ast` module

If you prefer `ast.load()` instead of `astload.load()`, you can do the following
to add a `load` function to the `ast` module directly:

```pycon
>>> import astload
>>> astload.install()
>>> import ast
>>> tree = ast.parse('print(2 + 2)')
>>> copy_tree = ast.load(ast.dump(tree))
>>> ast.unparse(copy_tree)
'print(2 + 2)'
```

### `astpretty` support

`astload` supports `astpretty` output also:

```pycon
>>> ast_string = astpretty.pformat(ast.parse('1 == 2'))
>>> print(ast_string)
Module(
    body=[
        Expr(
            lineno=1,
            col_offset=0,
            end_lineno=1,
            end_col_offset=6,
            value=Compare(
                lineno=1,
                col_offset=0,
                end_lineno=1,
                end_col_offset=6,
                left=Constant(lineno=1, col_offset=0, end_lineno=1, end_col_offset=1, value=1, kind=None),
                ops=[Eq()],
                comparators=[Constant(lineno=1, col_offset=5, end_lineno=1, end_col_offset=6, value=2, kind=None)],
            ),
        ),
    ],
    type_ignores=[],
)
>>> tree = astload.load(ast_string)
>>> astpretty.pprint(tree)
Module(
    body=[
        Expr(
            lineno=1,
            col_offset=0,
            end_lineno=1,
            end_col_offset=6,
            value=Compare(
                lineno=1,
                col_offset=0,
                end_lineno=1,
                end_col_offset=6,
                left=Constant(lineno=1, col_offset=0, end_lineno=1, end_col_offset=1, value=1, kind=None),
                ops=[Eq()],
                comparators=[Constant(lineno=1, col_offset=5, end_lineno=1, end_col_offset=6, value=2, kind=None)],
            ),
        ),
    ],
    type_ignores=[],
)
```
