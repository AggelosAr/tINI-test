from os import getcwd, path, walk
from pathlib import Path
from typing import Optional

from ._internals.consts import SKIP_DIRS

from .misc.exceptions import CantFindRelativePathToRoot

# TODO test edge cases of file paths with .. / etc ...

# TODO update arg parser to accept exclude dir 

# what happens if dir of file is given but only function ? do we search? ...
# review the search proccess , seems kinda stupid 


class ModuleCollector:

    

    def __init__(self,
                 search_dir: Optional[str] = None, 
                 search_file: Optional[str] = None,
                 exclude_dir: Optional[str] = None,) -> None:
        
        # Check case that exclude_dir is trash not yet implemented
        self.SKIP_DIRS = {**{l: None for l in SKIP_DIRS}, exclude_dir: None}

        print(self.SKIP_DIRS)
        self.root = Path(getcwd())
        if search_dir and search_dir != '.':
            # here we need to connect the 2 dirs
            self.search_dir = search_dir

            dest_parts = path.split(self.search_dir)
            self.dest_prefix, _ = dest_parts

            if new_root := self.connect_d_to_d(self.root):
                self.root = new_root
            else:
                raise CantFindRelativePathToRoot
            
        self.test_modules: dict[str, list[str]] = {}

        self.search_file = search_file
        if self.search_file and not self.search_file.endswith('.py'):
            self.search_file = '%s.py' % (self.search_file, )

    def is_valid_test_file(self, file_name: str) -> bool:
        return all([
            file_name.startswith('test_'),
            file_name.endswith('.py')
        ])
    
    def connect_d_to_d(self, root: Path) -> Optional[Path]:
        
        parts = str(root).partition(self.search_dir)
        found_dir = sum(map(lambda x: x is str(), parts)) == 1
        found_dir |= path.normpath(self.search_dir) == self.dest_prefix

        if found_dir:
            return root
        
        for c_path, dirs, _ in walk(root):
            
            _, s = path.split(Path(c_path))

            if s in self.SKIP_DIRS:
                break 

            for _dir in dirs:
                
                res = self.connect_d_to_d(Path(path.join(root, _dir)))
                if res:
                    return res

        return None

    def walk_and_collect_test_files(self, root: Path) -> None:
        """
        Walk the directory tree and collect Python modules that:
        - contain a `tests` folder
        - gather all `test_*.py` files inside that folder
        """
        
        for c_path, dirs, files in walk(root):
            
            _, s = path.split(Path(c_path))

            if s in self.SKIP_DIRS:
                break 
        
            if s == 'tests':

                py_files = list(filter(lambda l: self.is_valid_test_file(l), files))
                
                self.test_modules[c_path] = py_files

                if self.search_file in py_files:
                    return

            else:

                for c_dir in dirs:
                    
                    self.walk_and_collect_test_files(Path(path.join(root, c_dir)))

    def normalize_file_names(self, names: list[str]) -> list[str]:
        return list(map(lambda l: l.replace('.py', ''), names))
    
    def path_to_python_module(self, path_name: str) -> str:
        return '.'.join(Path(path_name).parts).lstrip('.').lstrip('/').lstrip('.')
    
    def normalize_collected_data(self) -> None:
        # TODO do we need cd here ?
        cd = getcwd()

        updates = {}

        for path_name in self.test_modules.keys():
            
            # Since how recursion works when searching the directory for a 
            # specific file we have to cleanup the collected modules 
            # in order to filter them out and only select the requested file.
            if self.search_file and self.search_file not in self.test_modules[path_name]:
                continue

            common_prefix = path.commonprefix([cd, path_name])

            new_name = path.normpath(path_name.replace(common_prefix, str()))
        
            new_name = self.path_to_python_module(new_name)

            file_names = self.test_modules[path_name]
            if self.search_file:
                file_names = list(filter(lambda l: l == self.search_file, file_names))

            normalized_file_names = self.normalize_file_names(file_names)

            updates[new_name] = normalized_file_names

            
        self.test_modules = updates
