import os
from pathlib import Path


class ModuleCollector:

    SKIP_DIRS = {
        "__pycache__",
        ".venv",
        "venv",
        "env",
        "build",
        "dist",
        ".git",
        ".pytest_cache",
        ".mypy_cache",
        "node_modules",
    }

    def __init__(self) -> None:
        self.test_modules: dict[str, list[str]] = {}

    # @property
    # def modules(self) -> dict[str, list[str]]:
    #     self.normalize_test_modules()
    #     f_modules = {}
    #     for module, test_files in self.test_modules.keys():
    #         for test_file in test_files:
    #             f_modules[module] = '%s.%s' % (module, test_file)
    #     return f_modules
    
    def is_valid_test_file(self, file_name: str) -> bool:
        return all([
            file_name.startswith('test_'),
            file_name.endswith('.py')
        ])
    
    def walk_collect_test_files(self, root: Path) -> None:
        """
        Walk the directory tree and collect Python modules that:
        - contain a `tests` folder
        - gather all `test_*.py` files inside that folder
        """
        
        for current_path, dirs, files in os.walk(root):
            
            _, s = os.path.split(Path(current_path))

            if s in self.SKIP_DIRS:
                break 
        
            if s == 'tests':

                py_files = list(filter(lambda l: self.is_valid_test_file(l), files))
                self.test_modules[current_path] = py_files

            else:

                for c_dir in dirs:
                    
                    self.walk_collect_test_files(Path(os.path.join(root, c_dir)))

    def normalize_file_names(self, names: list[str]) -> list[str]:
        return list(map(lambda l: l.replace('.py', ''), names))
    
    def path_to_python_module(self, path_name: str) -> str:
        return '.'.join(Path(path_name).parts).lstrip('.').lstrip('/').lstrip('.')
    
    def normalize_test_modules(self) -> None:
        cd = os.getcwd()

        updates = {}

        for path_name in self.test_modules.keys():

            common_prefix = os.path.commonprefix([cd, path_name])

            new_name = os.path.normpath(path_name.replace(common_prefix, ''))
        
            new_name = self.path_to_python_module(new_name)

            normalized_file_names = self.normalize_file_names(self.test_modules[path_name])


            updates[new_name] = normalized_file_names

        self.test_modules = updates
