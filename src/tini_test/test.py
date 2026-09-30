import asyncio
from collections import deque
from functools import cached_property, lru_cache, partial
from importlib import import_module
from types import FunctionType
from typing import Callable, Optional

from tini_test._internals._registry import (_CONN, _MOCK_REGISTRY,
                                            _TEST_REGISTRY)
from tini_test._internals.consts import _LINE_CLEAR, _LINE_UP, _RESET
from tini_test.enums import Color, RunMode, Verbosity
from tini_test.misc.annotations import (DirectoryPath, Errors, FileName,
                                        MockId, TestCollectionSize,
                                        TestFunctionName, TestId,
                                        TestWrappedObject)
from tini_test.mock import MockDefinition
from tini_test.test_utils import Test


class TestCollection:
    
    def __init__(self,
                 verbosity: Verbosity,
                 module_path: DirectoryPath,
                 file: FileName) -> None:
        
        self.verbosity = verbosity
        
        self.module = import_module('%s.%s' % (module_path, file, ))

        self.decorated_tests: list[Callable] = []

        self.collector: dict[TestFunctionName, Test] = dict()

        self.file_name = self.module.__name__
    
    def __len__(self) -> TestCollectionSize:
        return self.total_tests
    
    @cached_property
    def module_name(self) -> str:
        return self.module.__name__
    
    @property
    def total_tests(self) -> TestCollectionSize:
        return len(self.decorated_tests)

    def parse_wraps(self,
                    _obj_id: MockId | TestId, 
                    conn: dict[MockId | TestId, set[MockId | TestId]]
                    ) -> tuple[TestFunctionName, TestWrappedObject]:


        mocks: list[MockDefinition] = []
        test_wrap: TestWrappedObject = None
        test_func: Optional[FunctionType] = None
        
        registered_tests = 0

        q = deque([_obj_id])
        visited = set()

        iterations = 0
        while q:

            if registered_tests > 1:
                raise RuntimeError('Multiple test functions found for object ID %s' % (_obj_id, ))

            current_id = q.popleft()
            
            if current_id in visited:
                continue

            iterations += 1

            visited.add(current_id)

            if current_id in _TEST_REGISTRY:
                
                test_wrap = _TEST_REGISTRY[current_id]
                registered_tests += 1


            elif current_id in _MOCK_REGISTRY:

                mock_wrap = _MOCK_REGISTRY[current_id]


                [_test_func, *definition] = mock_wrap()

            
                if (
                    hex(id(_test_func)) in conn # TODO are we sure?
                    and 'Mock.mock' not in repr(_test_func)
                    and 'Test.test' not in repr(_test_func)
                ):
                    test_func = _test_func
                else:
                    # print('FOUND TEST FUNCTION BUT IGNORING...\n')
                    ...


                if definition:
                    mocks.append(*definition)

            else:
                ...
                # print('\t[WARNING] SKIPPING SINCE NOT FOUND IN TEST OR MOCK REGISTRY')
            # Obj may be single wrapped or nested e.g. _wrapped


            if _next := conn.get(current_id):
                q.extend(_next)
            # print('\n\n-------------------\n\n')

        # !! If the test was not mocked we don't have to do anything special
        if iterations < 3: # TODO FIX 
            return str(test_wrap.__closure__[-1].cell_contents.__name__), test_wrap
        # TODO also case no test found for the object ID
        # Move this error to Exceptions 
        # What do we do in this case ?
        # We collect the rest of the tests or we stop and inform ?
        # **Best solution is to add type annotate the Test in some way to inform the user he has made a mistake?
         # **is this even possible?
        if registered_tests == 0:
            raise RuntimeError('No test functions found for object ID %s' % (_obj_id, ))


        # Attach the correct test function to the test wrap
        _registered_test = test_wrap.__closure__[-1].cell_contents

        if 'Mock.mock' in repr(_registered_test) or 'Test.test' in repr(_registered_test):

            # There is the case where the last closure is the actual test pre-condition.
            # In that case we must also attach it.
            if hex(id(_registered_test)) in _MOCK_REGISTRY:
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

        # Also attach the mocks
        test_wrap = partial(test_wrap, 
                            _Test____mocks=mocks)

        return test_name, test_wrap

    
    def gather_tests(self, func_name: Optional[TestFunctionName] = None) -> list[TestFunctionName]:

        bi_con: dict[MockId | TestId, set[MockId | TestId]] = {}
        # TODO ...
        for k, v in _CONN.items():

            if k not in bi_con:
                bi_con[k] = set()
            bi_con[k].add(v)

            if v not in bi_con:
                bi_con[v] = set()
            bi_con[v].add(k)


        test_names = []

        for obj in dir(self.module):

            g_obj = getattr(self.module, obj)
           
            if not isinstance(g_obj, FunctionType):
                continue 

            _id = hex(id(g_obj))
            
            if not ((_id in _MOCK_REGISTRY) ^ (_id in _TEST_REGISTRY)):
                continue

            test_name, t_obj = self.parse_wraps(_obj_id=_id, conn=bi_con)

            if func_name and test_name != func_name:
                continue
            
            test_names.append(test_name)
            
            test_obj = partial(t_obj,
                               _Test____collector=self.collector,
                               _Test____verbosity=self.verbosity)
            
            self.decorated_tests.append(test_obj)


        return test_names
    
    def populate_tests(self) -> None:
        list(map(lambda dec_test_case: dec_test_case(), self.decorated_tests))

    def sort_tests(self) -> None:
        self.collector = dict(sorted(self.collector.items(), 
                                     key=lambda kv: kv[1].is_fail))
    
    def box_tests(self) -> None:
        list(map(lambda test_case: test_case.box_test(self.verbosity), self.collector.values()))

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

        # Cap the progress bar. # TODO broken on async?
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
    def _pprint(mode: RunMode) -> Errors:
        
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
    def run_tests(self) -> None:
        self.box_tests()
        
    @_pprint(RunMode.ASYNC)
    async def arun_tests(self) -> None:
        await self.abox_tests()
       