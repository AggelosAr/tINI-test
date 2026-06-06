import asyncio
from functools import cached_property, partial
from importlib import import_module
from types import FunctionType
from typing import Callable, Optional

from ._internals.consts import _LINE_CLEAR, _LINE_UP, _RESET
from .enums import Color, Verbosity
from .misc.annotations import (DirectoryPath, Errors, FileName,
                               TestCollectionSize, TestFunctionName)
from .test_utils import Test


class TestCollection:
    
    def __init__(self,
                 verbosity: Verbosity,
                 module_path: DirectoryPath,
                 file: FileName) -> None:
        
        self.verbosity = verbosity

        self.module = import_module('%s.%s' % (module_path, file, ))

        self.decorated_tests: list[Callable] = []

        self.collector: dict[str, Test] = dict()

        self.file_name = self.module.__name__
    
    @cached_property
    def module_name(self) -> str:
        return self.module.__name__
    
    @property
    def total_tests(self) -> TestCollectionSize:
        return len(self.decorated_tests)

    def get_summary_info(self):
        ...

    def gather_tests(self, func_name: Optional[TestFunctionName] = None) -> list[TestFunctionName]:

        test_names = []

        for obj in dir(self.module):

            g_obj = getattr(self.module, obj)
            
            if not all([isinstance(g_obj, FunctionType), 
                        hasattr(g_obj, '_xyz_is_a_test_case_uwu')]):
                continue 
            # TODO xxx
            test_name = str(g_obj.__closure__[-1].cell_contents.__name__)
            if func_name and test_name != func_name:
                continue
            
            test_names.append(test_name)

            test_obj = partial(g_obj, 
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
        raise NotImplementedError
    
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

        # Cap the progress bar. # TODO broken on async
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

    def run_tests(self) -> Errors:
        
        errors = 0

        print('Running tests for < %s >\n' % (self.file_name, ))

        self.populate_tests()
        self.box_tests()

        if self.verbosity == Verbosity.SORT:
            self.sort_tests()

        match self.verbosity:
            case Verbosity.NORMAL | Verbosity.SORT:
                errors = self.show_test_results_non_minimal()

            case Verbosity.MINIMAL | Verbosity.MINIMAL_NO_STACK | Verbosity.SUPER_MINIMAL:
                errors = self.show_test_results_minimal()
        
        print()
        return errors
    
    async def arun_tests(self) -> Errors:
        
        errors = 0

        print('Running tests for < %s >\n' % (self.file_name, ))

        self.populate_tests()

        await self.abox_tests()

        if self.verbosity == Verbosity.SORT:
            self.sort_tests()

        match self.verbosity:
            case Verbosity.NORMAL | Verbosity.SORT:
                errors = self.show_test_results_non_minimal()

            case Verbosity.MINIMAL | Verbosity.MINIMAL_NO_STACK | Verbosity.SUPER_MINIMAL:
                
                errors = self.show_test_results_minimal()
        
        print()
        return errors
