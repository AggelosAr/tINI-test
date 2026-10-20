import ast
from importlib.machinery import ModuleSpec
from pathlib import Path
from typing import no_type_check

from tini_test.misc.annotations import TestFunctionName


# TODO 
decorators = {'Test.case', 'Mock.mock', 'Shared', 'Isolate'}


class AstParser:

    def __init__(self, source: str, filename: str) -> None:
        self.root_node = ast.parse(source, filename=filename)
        self.source_lines = source.splitlines()

    @classmethod
    def from_spec(cls, spec: ModuleSpec) -> 'AstParser':
        return cls.from_path(spec.origin)

    @classmethod
    def from_path(cls, path: str | Path) -> 'AstParser':
        with open(path, 'r', encoding='utf-8') as f:
            return cls(f.read(), str(path))

    @classmethod
    def from_file_read(cls, data: str, filename: str = '<string>') -> 'AstParser':
        return cls(data, filename)
    
    @no_type_check
    def extract_line_to_statement(self) -> dict[int, int]:
        """Map every line to the id (starting at 1) of the statement that spans it.

        Compound statements (def, if, try, ...) only own their header, their bodies are
        separate statements. `case` and `except` clauses count as statements too.
        Bare strings (docstrings) and non statement lines (comments, blanks, else/finally)
        are not mapped.
        """
        statements = [
            node for node in ast.walk(self.root_node)
            if isinstance(node, (ast.stmt, ast.match_case, ast.ExceptHandler))
            and not (isinstance(node, ast.Expr)
                     and isinstance(node.value, ast.Constant)
                     and isinstance(node.value.value, str))
        ]

        def first_node(n):
            # match_case has no position of its own, its pattern is its first token
            return n.pattern if isinstance(n, ast.match_case) else n

        statements.sort(key=lambda n: (first_node(n).lineno, first_node(n).col_offset))

        line_to_statement: dict[int, int] = {}
        statement_id = 0

        for node in statements:
            start = min([first_node(node).lineno]
                        + [d.lineno for d in getattr(node, 'decorator_list', [])])

            block = getattr(node, 'body', None) or getattr(node, 'cases', None)
            if block:
                first = block[0]
                first_line = first_node(first).lineno
                # An inline body (`def f(\n x): ...`) sits on the last header line, so it
                # is part of the header, otherwise it would be a separate, never run, statement.
                inline = hasattr(first, 'col_offset') and bool(
                    self.source_lines[first_line - 1][:first.col_offset].strip()
                )
                end = first_line if inline else max(start, first_line - 1)
            else:
                end = node.end_lineno or node.lineno

            # An inline body (`if x: y`) shares its line with the header, the header wins.
            lines = [n for n in range(start, end + 1) if n not in line_to_statement]
            if not lines:
                continue

            statement_id += 1
            for line in lines:
                line_to_statement[line] = statement_id

        return line_to_statement

    @no_type_check
    def extract_top_level_import_lines(self) -> set[int]:
        """Lines executed once at import time by every top level node.

        Nodes with a nested block (def, class, if, try, ...) only contribute their header,
        since the block itself may never run.
        """
        lines: set[int] = set()

        for node in self.root_node.body:
            start = min([node.lineno] + [d.lineno for d in getattr(node, 'decorator_list', [])])

            block = getattr(node, 'body', None) or getattr(node, 'cases', None)
            if block:
                first = block[0]
                # match_case has no lineno of its own
                end = getattr(first, 'lineno', None) or first.pattern.lineno
                lines.update(range(start, max(end, node.lineno + 1)))
            else:
                lines.update(range(start, (node.end_lineno or node.lineno) + 1))

        return lines

    def get_top_level_functions(self) -> list[ast.FunctionDef]:
        return [node for node in self.root_node.body if isinstance(node, ast.FunctionDef)]

    def get_decorator_names(self, func: ast.FunctionDef) -> set[str]:
        names: set[str] = set()

        for dec in func.decorator_list:

            if isinstance(dec, ast.Call):
                dec = dec.func

            if isinstance(dec, (ast.Name, ast.Attribute)):
                names.add(ast.unparse(dec))

        return names
    
    def is_decorated_with(self, func: ast.FunctionDef) -> bool:
        return not self.get_decorator_names(func).isdisjoint(decorators)

    def extract_decorated_test_names(self) -> list[TestFunctionName]:
        return [fn.name for fn in filter(self.is_decorated_with, self.get_top_level_functions())]
    