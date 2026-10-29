import ast
from importlib.machinery import ModuleSpec
from pathlib import Path
from typing import no_type_check

from tini_test._internals.consts import E_DEC as decorators
from tini_test.misc.annotations import (CodeLineNumber, StatementId,
                                        TestFunctionName)


class AstParser:

    def __init__(self, source: str, filename: str) -> None:
        self.root_node = ast.parse(source, filename=filename)
        self.source_lines = source.splitlines()

    @classmethod
    def from_spec(cls, spec: ModuleSpec) -> 'AstParser':
        if spec.origin is None:
            raise ValueError('ModuleSpec has no origin') # TODO this is internal tINI-test exception?
        return cls.from_path(spec.origin)

    @classmethod
    def from_path(cls, path: str | Path) -> 'AstParser':
        with open(path, 'r', encoding='utf-8') as f:
            return cls(f.read(), str(path))

    @classmethod
    def from_file_read(cls, data: str, filename: str = '<string>') -> 'AstParser':
        return cls(data, filename)

    # def extract_line_to_statement(self) -> dict[CodeLineNumber, StatementId]:
    #     tree = ast.parse(self.root_node)
    #     result: dict[CodeLineNumber, StatementId] = {}
    #     statement_id = 0

    #     for node in ast.walk(tree):
    #         if not isinstance(node, ast.stmt):
    #             continue

    #         statement_id += 1

    #         for line in range(node.lineno, node.end_lineno + 1):
    #             result[line] = statement_id

    #     return result
    
    @no_type_check                                                                              #comment
    def extract_line_to_statement(self) -> dict[CodeLineNumber, StatementId]:                   #comment
        """Map every line to the id (starting at 1) of the statement that spans it.#comment

        Compound statements (def, if, try, ...) only own their header, their bodies are
        separate statements. `case` and `except` clauses count as statements too.
        Bare strings (docstrings) and non statement lines (comments, blanks, else/finally)
        are not mapped.
        """                                                                                     #comment
        statements = [                                                                          #comment
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

        line_to_statement: dict[CodeLineNumber, StatementId] = {}
        statement_id = 0

        for node in statements:
            # Every decorator is its own statement, the header then starts at the `def`/`class` line.
            for decorator in getattr(node, 'decorator_list', []):
                lines = [n for n in range(decorator.lineno, (decorator.end_lineno or decorator.lineno) + 1)
                         if n not in line_to_statement]
                if lines:
                    statement_id += 1
                    for line in lines:
                        line_to_statement[line] = statement_id

            start = first_node(node).lineno
            block = getattr(node, 'body', None) or getattr(node, 'cases', None)
            if block:
                first = block[0]
                first_line = min([first_node(first).lineno]
                                 + [d.lineno for d in getattr(first, 'decorator_list', [])])
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

    def extract_top_level_lines(self) -> list[CodeLineNumber]:
        lines: set[CodeLineNumber] = set()
        self._extract_top_level_lines(self.root_node.body, lines)
        return list(lines)

    def _extract_top_level_lines(self, nodes: list[ast.stmt], lines: set[CodeLineNumber]) -> None:
        for node in nodes:
            start = min([node.lineno] + [d.lineno for d in getattr(node, 'decorator_list', [])])

            block = getattr(node, 'body', None) or getattr(node, 'cases', None)
            if block:
                first = block[0]
                # match_case has no lineno of its own
                end = min([getattr(first, 'lineno', None) or first.pattern.lineno]
                          + [d.lineno for d in getattr(first, 'decorator_list', [])])
                
                lines.update(*[range(start, max(end, node.lineno + 1))])

                # A class body runs at definition time, unlike a function body.
                if isinstance(node, ast.ClassDef):
                    self._extract_top_level_lines(block, lines)
            else:
                lines.update(*[range(start, (node.end_lineno or node.lineno) + 1)])

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
    