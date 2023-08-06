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
>>> print(ast.unparse(copy_tree))
print(2 + 2)
```
