import ast
from importlib.machinery import ModuleSpec
from typing import no_type_check

from tini_test.misc.annotations import TestFunctionName


class AstParser:

    @no_type_check
    def __init__(self, from_spec: ModuleSpec) -> None:

        if isinstance(from_spec, ModuleSpec):
            with open(from_spec.origin, 'r', encoding='utf-8') as f:
                source = f.read()
                filename = from_spec.origin

        self.root_node = ast.parse(source, filename=filename)

    @no_type_check
    def extract_top_level_function_nodes(self) -> list[ast.FunctionDef]:
        return [node for node in self.root_node.body if isinstance(node, ast.FunctionDef)]

    @no_type_check
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
