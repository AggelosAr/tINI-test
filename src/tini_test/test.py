import asyncio
import importlib.util
from collections import deque
from functools import cached_property, lru_cache, partial
from types import FunctionType, ModuleType
from typing import Callable, Optional, no_type_check

from tini_test._internals.consts import _LINE_CLEAR, _LINE_UP, _RESET
from tini_test.enums import Color, RunMode, Verbosity
from tini_test.misc.annotations import (C_REG, M_REG, S_REG, T_REG,
                                        DirectoryPath, Errors, FileName,
                                        GlobalRegistry, MockId,
                                        MockWrappedObject, PartialObject,
                                        SharedId, TestCollectionSize,
                                        TestFunctionName, TestId,
                                        TestWrappedObject,
                                        _ReverseWrapConnections)
from tini_test.misc.exceptions import (DuplicateMockRegisteredOnTest,
                                       MockWasUsedOnWithoutTestDecorator,
                                       SharedVarAlreadyDefined,
                                       SharedWasUsedOnWithoutTestDecorator,
                                       TestDecoratorUsedMoreThanOnce)
from tini_test.mock import MockDefinition
from tini_test.shared import MetaSharedVar, SharedVar
from tini_test.test_utils import Test


class TestCollection:
    
    def __init__(self,
                 verbosity: Verbosity,
                 module_path: DirectoryPath,
                 file: FileName) -> None:
        
        self.verbosity = verbosity

        self._TEST_REGISTRY   : T_REG = {}
        self._MOCK_REGISTRY   : M_REG = {}
        self._SHARED_REGISTRY : S_REG = {}
        self._CONN_REGISTRY   : C_REG = {}

        context: GlobalRegistry = {
            '_TEST_REGISTRY'  : self._TEST_REGISTRY,
            '_MOCK_REGISTRY'  : self._MOCK_REGISTRY,
            '_SHARED_REGISTRY': self._SHARED_REGISTRY,
            '_CONN_REGISTRY'  : self._CONN_REGISTRY,
        }
      
        self.module = self.import_with_context('%s.%s' % (module_path, file, ), context)
        
        self.decorated_tests: list[PartialObject] = []

        self.collector: dict[TestFunctionName, Test] = dict()

        self.file_name = self.module.__name__

        self.shared_meta: Optional[MetaSharedVar] = None
    
    def __len__(self) -> TestCollectionSize:
        return self.total_tests
    
    @cached_property
    def module_name(self) -> str:
        return self.module.__name__
    
    @cached_property
    def bi_con(self) -> _ReverseWrapConnections:
        return self.reverse_connections()

    @property
    def total_tests(self) -> TestCollectionSize:
        return len(self.decorated_tests)

    def import_with_context(self, module_name: str, context: GlobalRegistry) -> ModuleType:

        spec = importlib.util.find_spec(module_name)
        # @coverage
        if spec is None:
            raise RuntimeError('Cannot find module named %s' % (module_name, ))
        if spec.loader is None:
            raise RuntimeError('Cannot load module named %s' % (module_name, ))
        
        module = importlib.util.module_from_spec(spec)

        module.__dict__.update(context)

        spec.loader.exec_module(module)        

        return module
    
    def reverse_connections(self) -> _ReverseWrapConnections:
        bi_con: _ReverseWrapConnections = {}

        for k, v in self._CONN_REGISTRY.items():

            if k not in bi_con:
                bi_con[k] = set()
            bi_con[k].add(v)

            if v not in bi_con:
                bi_con[v] = set()
            bi_con[v].add(k)

        return bi_con

    # XXX
    # remove magic strings.

    @no_type_check 
    def parse_wraps(self, _obj_id: TestId | MockId | SharedId) -> tuple[TestFunctionName, TestWrappedObject]:

        # General case. We currently stop collecting on the first error. Should we continue?

        

        test_wrap: TestWrappedObject
        test_func: Optional[FunctionType
                            |TestWrappedObject
                            |MockWrappedObject] = None # ?
        registered_tests = 0

        mocks: list[MockDefinition] = []
        unique_mocks: set[str] = set()
        found_mocks = 0

        shared_vars: list[SharedVar] = []
        unique_shared_vars: set[str] = set()
        found_shared_vars = 0

        # In case of any error we still need to unwrap to get the test name...
        aborted: list[Callable[[TestFunctionName], DuplicateMockRegisteredOnTest] 
                      | Callable[[TestFunctionName], SharedVarAlreadyDefined]] = [] 

        visited = set()
        q = deque([_obj_id])
        
        while q:

            current_id = q.popleft()
            
            if current_id in visited:
                continue

            visited.add(current_id)

            if _next := self.bi_con.get(current_id):
                q.extend(_next)
            
            if current_id in self._TEST_REGISTRY:
                test_wrap = self._TEST_REGISTRY[current_id]
                registered_tests += 1

            else:
                if aborted:
                    continue

            if current_id in self._MOCK_REGISTRY:
                mock_wrap = self._MOCK_REGISTRY[current_id]
                found_mocks += 1

                [_test_func, *_definition] = mock_wrap()

                if (
                    hex(id(_test_func)) in self.bi_con
                    and 'Mock.mock' not in repr(_test_func)
                    and 'Test.test' not in repr(_test_func)
                    and 'Shared' not in repr(_test_func)
                ):
                    test_func = _test_func

                if _definition:

                    definition, *_ = _definition
                
                    if definition.mock.__name__ in unique_mocks:
                        aborted.append(
                            lambda test_name: 
                                DuplicateMockRegisteredOnTest
                                    (
                                        mock_name=definition.mock.__name__, 
                                        test_name=test_name
                                    )
                            )
                    
                    unique_mocks.add(definition.mock.__name__)
                    mocks.append(definition)

            if current_id in self._SHARED_REGISTRY:
                shared_wrap = self._SHARED_REGISTRY[current_id]
                found_shared_vars += 1

                [_test_func, *_shared_holder] = shared_wrap()

                if (
                    hex(id(_test_func)) in self.bi_con
                    and 'Mock.mock' not in repr(_test_func)
                    and 'Test.test' not in repr(_test_func)
                    and 'Shared' not in repr(_test_func)
                ):
                    test_func = _test_func

                if _shared_holder:

                    _shared_vars, *_ = _shared_holder

                    for _shared_var in _shared_vars:
                        var_name = _shared_var.__key__

                        if var_name in unique_shared_vars:
                            aborted.append(
                                lambda test_name: 
                                    SharedVarAlreadyDefined
                                        (
                                            var_name=var_name, 
                                            test_name=test_name
                                        )
                                )
                            break

                        unique_shared_vars.add(var_name)

                    shared_vars.extend(_shared_vars)

      
        if registered_tests == 0:
            if found_mocks:
                _t = test_func or str(mock_wrap.__closure__[-1].cell_contents.__name__)
                raise MockWasUsedOnWithoutTestDecorator(_t)
            if found_shared_vars:
                _t = test_func or str(shared_wrap.__closure__[-1].cell_contents.__name__)
                raise SharedWasUsedOnWithoutTestDecorator(_t)

        no_mocks = not mocks and not found_mocks
        no_shared_vars = not shared_vars and not found_shared_vars
        is_alone = no_mocks and no_shared_vars

        if registered_tests > 1 and is_alone:
            _t = test_func or str(test_wrap.__closure__[-1].cell_contents.__name__)
            raise TestDecoratorUsedMoreThanOnce(_t)
        
        if is_alone:
            return str(test_wrap.__closure__[-1].cell_contents.__name__), test_wrap

        # Attach the correct test function to the test wrap
        _registered_test = test_wrap.__closure__[-1].cell_contents

        if registered_tests > 1 and not is_alone:
            raise TestDecoratorUsedMoreThanOnce(_registered_test)
                
        if ('Mock.mock' in repr(_registered_test) 
            or 'Test.test' in repr(_registered_test)
            or 'Shared' in repr(_registered_test)):

            # There is the case where the last closure is the actual test pre-condition.
            # In that case we must also attach it.
            if hex(id(_registered_test)) in self._MOCK_REGISTRY:
                test_wrap = partial(test_wrap,  
                                    _Test____test_func=test_func)
                test_name = test_func.__name__
            elif hex(id(_registered_test)) in self._SHARED_REGISTRY:
                test_wrap = partial(test_wrap,  
                                    _Test____test_func=test_func)
                test_name = test_func.__name__
            else:
                test_wrap.__closure__[-1].cell_contents.__code__ = test_func.__code__
                
                test_name = str(test_wrap.__closure__[-1].cell_contents.__name__)
     
        else:

            # We need to see if the test is already attached
            if _registered_test == test_func.__closure__[-1].cell_contents:
                test_name = _registered_test.__name__
                ...
            else:

                test_name = test_func.__name__
                test_wrap = partial(test_wrap,  
                                    _Test____test_func=test_func)


        if aborted:
            raise aborted[0](test_name)# XXX raise the exeption from the correct line. 

        for shared_var in shared_vars:
            SharedVar.add_scope(shared_var, test_name)
        
        # Also attach the mocks and the shared variables
        test_wrap = partial(test_wrap, 
                            _Test____mocks=mocks,
                            _Test____shared_vars=shared_vars)

        return test_name, test_wrap


    def gather_tests(self, func_name: Optional[TestFunctionName] = None) -> list[TestFunctionName]:

        test_names = []

        for obj in dir(self.module):

            g_obj = getattr(self.module, obj)

            if isinstance(g_obj, MetaSharedVar):
                self.shared_meta = g_obj
          
            if not isinstance(g_obj, FunctionType):
                continue 

            _id = hex(id(g_obj))
            
            if not (  (_id in self._TEST_REGISTRY) 
                    ^ (_id in self._MOCK_REGISTRY) 
                    ^ (_id in self._SHARED_REGISTRY)):
                continue

            test_name, t_obj = self.parse_wraps(_obj_id=_id)

            if func_name and test_name != func_name:
                continue

            test_obj = partial(t_obj,
                               _Test____collector=self.collector,
                               _Test____verbosity=self.verbosity)
            
            test_names.append(test_name)
            self.decorated_tests.append(test_obj)

        return test_names

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
    
    def show_test_results_non_minimal(self) -> Errors:

        failed_tests = 0

        for idx, test_case in enumerate(self.collector.values(), start=1):
            
            print("[ %s / %s ]\n\tTEST\t—›  %s\n\t\t——› %s\n\n\n%s" 
                  % (idx, 
                     self.total_tests, 
                     self.module_name,
                     test_case.test_name, 
                     str(test_case), ))


            failed_tests += test_case.is_fail

        return failed_tests

    def show_test_results_minimal(self) -> Errors:

        # Cap the progress bar.
        bucket_size = 18

        e_symbol = ('%s   %s' % (Color.WHITE.value, _RESET, ))
        s_symbol = ('%s • %s' % (Color.RED.value, _RESET, ))
        f_symbol = ('%s • %s' % (Color.GREEN.value, _RESET, ))

        previous_progress: list[list[str]] = []
        progress = ['[']+[e_symbol for _ in range(bucket_size)]+[']']

        errors = 0
        failed_tests, stacktraces = [], []


        for idx, test_case in enumerate(self.collector.values()):
            
            bucket_idx = (idx)%bucket_size

            if test_case.is_fail:

                failed_tests.append(test_case.test_name)
                stacktraces.append(test_case.fail_reasons)

                progress[bucket_idx+1] = s_symbol

            else:
                progress[bucket_idx+1] = f_symbol


            print(''.join(progress))
            # sys.stdout.flush()

            if idx != self.total_tests-1:

                print(_LINE_UP, end=_LINE_CLEAR)
            

            if bucket_idx+1==bucket_size:

                for _ in range(len(previous_progress)):
                   
                    print(_LINE_UP, end=_LINE_CLEAR)

                previous_progress.append(progress)

       
                for _ in range(len(previous_progress)):
                    print(''.join(previous_progress[_]))

                progress = ['[']+[e_symbol for _ in range(bucket_size)]+[']']
            
        errors = len(failed_tests)

        if self.verbosity == Verbosity.SUPER_MINIMAL:
            return errors
        
        print('\nFinished running tests for < %s >\n' % (self.file_name, ))
        print('Tests passed: [ %d / %d ]\n' 
            % (self.total_tests - errors, self.total_tests, ))
        
        if not failed_tests:
            print('...\n')
            return errors
        
        if self.verbosity == Verbosity.MINIMAL_NO_STACK:

            print('\nErrors:')

            for failed_test in failed_tests:
                print('\t—› %s' % (failed_test, ))

            print('...\n')
            return errors
        
        idx = 0
        for test, traces in zip(failed_tests, stacktraces):
            idx += 1
            print('\nTEST\t—›  %s\n\t——› %s\n' % (self.module_name, test, ))

            for trace in traces:

                print(trace)

                if idx != errors:
                    print('%s ~~~ %s' % (Color.RED.value, _RESET, ))
    
        print('...\n')
        return errors
    
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

                        async def ____wrapper() -> Errors:

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
        if self.shared_meta:
            # Disallow generation during runtime.
            self.shared_meta.toggle()

    def __cleanup(self) -> Errors:
        if self.verbosity == Verbosity.SORT:
            self.sort_tests()

        match self.verbosity:
            case Verbosity.NORMAL | Verbosity.SORT:
                errors = self.show_test_results_non_minimal()

            case Verbosity.MINIMAL | Verbosity.MINIMAL_NO_STACK | Verbosity.SUPER_MINIMAL:
                errors = self.show_test_results_minimal()
        
        print()
    
        return errors
    
    @_pprint(RunMode.SYNC)
    def run_tests(self) -> Errors:
        self.box_tests()
        
    @_pprint(RunMode.ASYNC)
    async def arun_tests(self) -> Errors:
        await self.abox_tests()
       