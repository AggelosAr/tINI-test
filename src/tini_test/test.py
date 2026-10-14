import asyncio
import importlib.util
from collections import deque
from functools import cached_property, lru_cache, partial
from importlib.machinery import ModuleSpec
from types import FunctionType, ModuleType
from typing import Callable, Counter, Optional

from tini_test._internals._ast_utils import AstParser
from tini_test._internals.consts import (_C_REG, _I_REG, _LINE_CLEAR, _LINE_UP,
                                         _M_REG, _RESET, _S_REG, _T_REG)
from tini_test.enums import Color, RunMode, Verbosity
from tini_test.misc.annotations import (C_Reg, DirectoryPath, DotPythonPath,
                                        Errors, FileName, I_Reg, M_Reg,
                                        PartialObject, S_Reg, T_Reg,
                                        TestCollectionSize, TestFunctionName,
                                        _ReverseWrapConnections)
from tini_test.misc.exceptions import DuplicateTestFound
from tini_test.mock import MockDefinition
from tini_test.shared import MetaSharedVar, SharedVar
from tini_test.test_utils import _XTest
from tini_test.wrap_utils import DecoratedTestChain


class TestCollection:
    
    def __init__(self,
                 verbosity: Verbosity,
                 module_path: DirectoryPath,
                 file: FileName,
                 shared_meta: MetaSharedVar) -> None:
        
        self.module_path = module_path
        self.verbosity = verbosity
        self.file_name = file

        self.shared_meta = shared_meta
        
        self.TEST_REGISTRY       : T_Reg = {}
        self.MOCK_REGISTRY       : M_Reg[MockDefinition] = {}
        self.SHARED_REGISTRY     : S_Reg[SharedVar] = {}
        self.ISOLATE_REGISTRY    : I_Reg = {}
        self.CONNECTION_REGISTRY : C_Reg = {}

        self.module: Optional[ModuleType] = None
        
        self.decorated_tests: list[PartialObject] = []
        self.collector: dict[TestFunctionName, _XTest] = dict()

    def __len__(self) -> TestCollectionSize:
        return self.total_tests
    
    @cached_property
    def module_name(self) -> FileName:
        return self.file_name
    
    @cached_property
    def bi_con(self) -> _ReverseWrapConnections:
        return self.reverse_connections()

    @cached_property
    def dot_python_path(self) -> DotPythonPath:
        return '%s.%s' % (self.module_path, self.file_name, )
    
    @property
    def total_tests(self) -> TestCollectionSize:
        return len(self.decorated_tests)

    @property
    def has_tests(self) -> bool:
        return self.total_tests > 0
    
    @staticmethod
    def get_module_loader(module_name: DotPythonPath) -> tuple[ModuleSpec, ModuleType]:
        spec = importlib.util.find_spec(module_name)
        # @coverage
        if spec is None:
            raise RuntimeError('Cannot find module named %s' % (module_name, ))

        module = importlib.util.module_from_spec(spec)
        return spec, module

    def update_globals(self, module: ModuleType) -> None:
        context = {
            _T_REG : self.TEST_REGISTRY,
            _M_REG : self.MOCK_REGISTRY,
            _S_REG : self.SHARED_REGISTRY,
            _I_REG : self.ISOLATE_REGISTRY,
            _C_REG : self.CONNECTION_REGISTRY,
        }
        module.__dict__.update(context)

    def _import(self) -> None:
        spec, module = self.get_module_loader(self.dot_python_path)

        self.validate_duplicate_tests(spec)
        
        self.update_globals(module)
        
        self.module = module

        if spec.loader is None:
            raise RuntimeError('Cannot load module named %s' % (self.dot_python_path, ))
        spec.loader.exec_module(module)

    def validate_duplicate_tests(self, spec: ModuleSpec) -> None:
        top_level_test_names = AstParser(spec).extract_decorated_test_names()
        names = Counter(top_level_test_names)
        duplicates = {n for n in names if names[n] > 1}
        if duplicates:
            raise DuplicateTestFound(list(duplicates))
        
    def reset_shared_meta(self) -> None:
        self.shared_meta.reset()

    def raise_for_globals(self) -> None:
        self.shared_meta.raise_for_globals()

    def reverse_connections(self) -> _ReverseWrapConnections:
        bi_con: _ReverseWrapConnections = {}

        for k, v in self.CONNECTION_REGISTRY.items():

            if k not in bi_con:
                bi_con[k] = set()
            bi_con[k].add(v)

            if v not in bi_con:
                bi_con[v] = set()
            bi_con[v].add(k)

        return bi_con

    def gather_tests(self, func_name: Optional[TestFunctionName] = None) -> list[TestFunctionName]:

        test_names = set()

        for obj in dir(self.module):

            g_obj = getattr(self.module, obj)

            if isinstance(g_obj, MetaSharedVar):
                self.shared_meta = g_obj
          
            if not isinstance(g_obj, FunctionType):
                continue 

            _id = hex(id(g_obj))
            
            if not (  (_id in self.TEST_REGISTRY) 
                    ^ (_id in self.MOCK_REGISTRY) 
                    ^ (_id in self.SHARED_REGISTRY)
                    ^ (_id in self.ISOLATE_REGISTRY)):
                continue

            # General case. We currently stop collecting on the first error.
            test_chain = DecoratedTestChain.resolve_chain(self.bi_con,
                                                          self.TEST_REGISTRY,
                                                          self.MOCK_REGISTRY,
                                                          self.SHARED_REGISTRY,
                                                          self.ISOLATE_REGISTRY,
                                                          _obj_id=_id)

            test_chain.raise_for_multiple_test_wraps()
            test_chain.raise_for_no_test_wraps()

            match test_chain.has_dependencies:

                case True:
                    test_wrap = test_chain.test_wrap
                    test_name, t_obj = str(test_wrap.__closure__[-1].cell_contents.__name__), test_wrap # type: ignore[index]
                case False:
                    test_name, t_obj = test_chain.resolve_dependencies(self.MOCK_REGISTRY,
                                                                       self.SHARED_REGISTRY,
                                                                       self.ISOLATE_REGISTRY)

                    test_chain.validate_dependencies(test_name)
                    
                    SharedVar.add_scope(test_chain.shared_vars, test_name)
                    t_obj = partial(t_obj, 
                                    _XTest____mocks=test_chain.mocks,
                                    _XTest____shared_vars=test_chain.shared_vars,
                                    _XTest____isolate=test_chain.isolate)
                
            
            if func_name and test_name != func_name:
                continue

            test_obj = partial(t_obj,
                               _XTest____collector=self.collector,
                               _XTest____verbosity=self.verbosity)

            test_names.add(test_name)
            self.decorated_tests.append(test_obj)

        # if len(test_names) != len(self.TEST_REGISTRY):
        #     raise DuplicateTestFound
        
        return list(test_names)

    def populate_tests(self) -> None:
        deque(map(lambda dec_test_case: dec_test_case(), self.decorated_tests))

    def sort_tests(self) -> None:
        self.collector = dict(sorted(self.collector.items(), key=lambda kv: kv[1].is_fail))
    
    def box_tests(self) -> None:
        deque(map(lambda test_case: test_case.box_test(self.verbosity), self.collector.values()))

    async def abox_tests(self) -> None:
        tasks = [test_case.abox_test(self.verbosity) for test_case in self.collector.values()]
        await asyncio.gather(*tasks)

    def sort_tests_based_on_source(self) -> None:
        ...
    
    @lru_cache
    def _pprint(mode: RunMode): # <<< !
        
        def _wrapper(runner: Callable):
            
            def __wrapper(self: 'TestCollection', *args, **kwargs):
                
                match mode:

                    case RunMode.SYNC:
                        
                        def ____wrapper() -> Errors:

                            self.__setup()
                            runner(self)
                            return self.__cleanup()
                        
                        ___wrapper = ____wrapper()

                    case RunMode.ASYNC:

                        async def ____wrapper() -> Errors: # type: ignore[misc]

                            self.__setup()
                            await runner(self)
                            return self.__cleanup()

                        ___wrapper = ____wrapper()
                        
                return ___wrapper
            
            return __wrapper
        
        return _wrapper

    def __setup(self) -> None:
        print('Running tests for < %s >\n' % (self.file_name, ))

        self.populate_tests()
        # Disallow generation during runtime.
        self.shared_meta.block()

    def __cleanup(self) -> Errors:
        if self.verbosity == Verbosity.SORT:
            self.sort_tests()

        match self.verbosity:
            case Verbosity.NORMAL | Verbosity.SORT:
                errors = Printer.show_test_results_non_minimal(self)

            case Verbosity.MINIMAL | Verbosity.MINIMAL_NO_STACK | Verbosity.SUPER_MINIMAL:
                errors = Printer.show_test_results_minimal(self)
        
        print()
    
        return errors
    
    @_pprint(RunMode.SYNC)
    def run_tests(self):
        self.box_tests()
        
    @_pprint(RunMode.ASYNC)
    async def arun_tests(self):
        await self.abox_tests()


class Printer:

    @staticmethod
    def show_test_results_non_minimal(collection: TestCollection) -> Errors:

            failed_tests = 0

            for idx, test_case in enumerate(collection.collector.values(), start=1):
                
                print("[ %s / %s ]\n\tTEST\t—›  %s\n\t\t——› %s\n\n\n%s" 
                    % (idx, 
                        collection.total_tests, 
                        collection.module_name,
                        test_case.test_name, 
                        str(test_case), ))


                failed_tests += test_case.is_fail

            return failed_tests

    @staticmethod
    def show_test_results_minimal(collection: TestCollection) -> Errors:

        # Cap the progress bar.
        bucket_size = 18

        e_symbol = ('%s   %s' % (Color.WHITE.value, _RESET, ))
        s_symbol = ('%s • %s' % (Color.RED.value, _RESET, ))
        f_symbol = ('%s • %s' % (Color.GREEN.value, _RESET, ))

        previous_progress: list[list[str]] = []
        progress = ['[']+[e_symbol for _ in range(bucket_size)]+[']']

        errors = 0
        failed_tests, stacktraces = [], []


        for idx, test_case in enumerate(collection.collector.values()):
            
            bucket_idx = (idx)%bucket_size

            if test_case.is_fail:

                failed_tests.append(test_case.test_name)
                stacktraces.append(test_case.fail_reasons)

                progress[bucket_idx+1] = s_symbol

            else:
                progress[bucket_idx+1] = f_symbol


            print(''.join(progress))
            # sys.stdout.flush()

            if idx != collection.total_tests-1:

                print(_LINE_UP, end=_LINE_CLEAR)
            

            if bucket_idx+1==bucket_size:

                for _ in range(len(previous_progress)):
                    
                    print(_LINE_UP, end=_LINE_CLEAR)

                previous_progress.append(progress)

        
                for _ in range(len(previous_progress)):
                    print(''.join(previous_progress[_]))

                progress = ['[']+[e_symbol for _ in range(bucket_size)]+[']']
            
        errors = len(failed_tests)

        if collection.verbosity == Verbosity.SUPER_MINIMAL:
            return errors
        
        print('\nFinished running tests for < %s >\n' % (collection.file_name, ))
        print('Tests passed: [ %d / %d ]\n' 
            % (collection.total_tests - errors, collection.total_tests, ))
        
        if not failed_tests:
            print('...\n')
            return errors
        
        if collection.verbosity == Verbosity.MINIMAL_NO_STACK:

            print('\nErrors:')

            for failed_test in failed_tests:
                print('\t—› %s' % (failed_test, ))

            print('...\n')
            return errors
        
        idx = 0
        for test, traces in zip(failed_tests, stacktraces):
            idx += 1
            print('\nTEST\t—›  %s\n\t——› %s\n' % (collection.module_name, test, ))

            for trace in traces:

                print(trace)

                if idx != errors:
                    print('%s ~~~ %s' % (Color.RED.value, _RESET, ))

        print('...\n')
        return errors
