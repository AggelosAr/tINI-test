from os import getcwd, path, walk
from pathlib import Path
from typing import Optional

from tini_test.misc.annotations import Directory, FileName

from ._internals.consts import SKIP_DIRS
from .misc.exceptions import CantFindRelativePathToRoot

# TODO update arg parser to accept exclude dir 

class ModuleCollector:

    def __init__(self,
                 search_dir: Directory, 
                 file_name: Optional[FileName] = None,
                 exclude_dir: Optional[Directory] = None,) -> None:
        
        # Check case that exclude_dir is trash not yet implemented
        self.SKIP_DIRS = {**{l: None for l in SKIP_DIRS}, exclude_dir: None}

        self.root = Path(getcwd())
        if search_dir != '.':
            # here we need to connect the 2 dirs
            self.search_dir = search_dir

            dest_parts = path.split(self.search_dir)
            self.dest_prefix, _ = dest_parts

            if new_root := self.connect_d_to_d(self.root):
                self.root = new_root
            else:
                raise CantFindRelativePathToRoot
            
        self.test_modules: dict[str, list[str]] = {}

        self.file_name = file_name
        if self.file_name and not self.file_name.endswith('.py'):
            self.file_name = '%s.py' % (self.file_name, )

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

    # Fix recursion paths 
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
                 
                if self.file_name in py_files:
                    return
                

            for c_dir in dirs:
                
                self.walk_and_collect_test_files(Path(path.join(root, c_dir)))

    def normalize_file_names(self, names: list[str]) -> list[str]:
        return list(map(lambda l: l.replace('.py', ''), names))
    
    def path_to_python_module(self, path_name: str) -> str:
        r = '.'.join(Path(path_name).parts)
        r = r.strip()
        while r and r[0] in {'.', '/', '\\'}:
            r = r[1:]
        while r and r[-1] in {'.', '/', '\\'}:
            r = r[:-1]
        return r
    
    def normalize_collected_data(self) -> None:
        # TODO do we need cd here ?
        cd = getcwd()

        updates = {}

        for path_name in self.test_modules.keys():
            
            # Since how recursion works when searching the directory for a 
            # specific file we have to cleanup the collected modules 
            # in order to filter them out and only select the requested file.
            if self.file_name and self.file_name not in self.test_modules[path_name]:
                continue

            common_prefix = path.commonprefix([cd, path_name])

            new_name = path.normpath(path_name.replace(common_prefix, str()))
        
            new_name = self.path_to_python_module(new_name)

            file_names = self.test_modules[path_name]
            if self.file_name:
                file_names = list(filter(lambda l: l == self.file_name, file_names))

            normalized_file_names = self.normalize_file_names(file_names)

            updates[new_name] = normalized_file_names

            
        self.test_modules = updates
