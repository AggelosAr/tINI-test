import ast
from importlib.machinery import ModuleSpec
from pathlib import Path

from tini_test.misc.annotations import TestFunctionName


class AstParser:

    def __init__(self, from_spec: ModuleSpec | Path) -> None:

        if isinstance(from_spec, ModuleSpec):
            with open(from_spec.origin, 'r', encoding='utf-8') as f:
                source = f.read()
                filename = from_spec.origin

        if isinstance(from_spec, Path):
            with open(from_spec, 'r', encoding='utf-8') as f:
                source = f.read()
                filename = from_spec

        self.root_node = ast.parse(source, filename=filename)

    def extract_function_calls_in_function_node(self, function_node: ast.FunctionDef) -> list[TestFunctionName]:
        calls: list[TestFunctionName] = []
        for node in ast.walk(function_node):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                calls.append(node.func.id)
        return calls

    def extract_top_level_function_nodes(self) -> list[ast.FunctionDef]:
        return [node for node in self.root_node.body if isinstance(node, ast.FunctionDef)]

    def extract_top_level_function_names(self) -> list[TestFunctionName]:
        return [fn.name for fn in self.extract_top_level_function_nodes()]

    def extract_top_level_function_nodes_with_test_decorator(self) -> list[ast.FunctionDef]:
        return [
            fn for fn in self.extract_top_level_function_nodes()
            if any(
                isinstance(dec, ast.Attribute) and dec.value.id == 'Test' and dec.attr == 'case'
                for dec in fn.decorator_list
            )
        ]

    def extract_decorated_test_names(self) -> list[TestFunctionName]:
        return [fn.name for fn in self.extract_top_level_function_nodes_with_test_decorator()]
