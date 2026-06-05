from functools import cached_property, partial
from importlib import import_module
from time import perf_counter
from types import FunctionType
from typing import Callable, Optional, TypeAlias

from ._internals.consts import _LINE_CLEAR, _LINE_UP, _RESET
from .enums import Color, Mode
from .misc.annotations import (Errors, TestName, TestSuiteResults,
                               TimeTakenForModule)
from .misc.exceptions import NotSupportedMode
from .test_utils import Test


class TestSuite:
    
    def __init__(self, 
                 module: str,
                 file: str,
                 mode: Optional[Mode | str] = Mode.SORT) -> None:
        
        if mode is None:
            mode = Mode.SORT

        match mode:
            case Mode.SORT:
                self.mode = Mode.SORT
            case Mode.SORT.value:
                self.mode = Mode.SORT
            case Mode.NORMAL:
                self.mode = Mode.NORMAL
            case Mode.NORMAL.value:
                self.mode = Mode.NORMAL
            case Mode.MINIMAL:
                self.mode = Mode.MINIMAL
            case Mode.MINIMAL.value:
                self.mode = Mode.MINIMAL
            case Mode.SUPER_MINIMAL:
                self.mode = Mode.SUPER_MINIMAL
            case Mode.SUPER_MINIMAL.value:
                self.mode = Mode.SUPER_MINIMAL
            case Mode.MINIMAL_NO_STACK:
                self.mode = Mode.MINIMAL_NO_STACK
            case Mode.MINIMAL_NO_STACK.value:
                self.mode = Mode.MINIMAL_NO_STACK
            case _:
                raise NotSupportedMode(msg=Mode.supported_modes())

        self.module = import_module('%s.%s' % (module, file, ))

        self.decorated_tests: list[Callable] = []

        self.collector: dict[str, Test] = dict()

        self.file_name = self.module.__name__

    @cached_property
    def module_name(self) -> str:
        return self.module.__name__
    
    @property
    def total_tests(self) -> int:
        return len(self.collector.values())
    
    def gather_tests(self, func_name: Optional[str] = None) -> list[TestName]:

        test_names = []

        for obj in dir(self.module):

            g_obj = getattr(self.module, obj)
            
            if not all([isinstance(g_obj, FunctionType), 
                        hasattr(g_obj, '_xyz_is_a_test_case_uwu')]):
                continue 
            
            test_name = str(g_obj.__closure__[-1].cell_contents.__name__)
            if func_name and test_name != func_name:
                continue
            
            test_names.append(test_name)

            test_obj = partial(g_obj, _Test____collector=self.collector)
            self.decorated_tests.append(test_obj)

        return test_names
    
    def populate_tests(self) -> None:
        list(map(lambda l: l(), self.decorated_tests))

    def sort_tests(self) -> None:
        self.collector = dict(sorted(self.collector.items(), 
                                     key=lambda kv: kv[1].is_fail))
        
    def box_tests(self) -> None:
        list(map(lambda l: l.box_test(self.mode), self.collector.values()))

    def sort_tests_based_on_source(self) -> None:
        raise NotImplementedError
    
    def show_test_results_non_minimal(self, start_timer: float) -> tuple[Errors, TimeTakenForModule]:

        failed_tests = 0

        for idx, test_case in enumerate(self.collector.values(), start=1):
            
            
            print("[ %s / %s ]\n\tTEST\t—›  %s\n\t\t——› %s\n\n\n%s" 
                  % (idx, 
                     self.total_tests, 
                     self.module_name,
                     test_case.test_name, 
                     str(test_case), ))
        

            failed_tests += test_case.is_fail

        return failed_tests, perf_counter() - start_timer

    def show_test_results_minimal(self, start_timer: float) -> tuple[Errors, TimeTakenForModule]:

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
            # import time
            # time.sleep(0.3)
            bucket_idx = (idx)%bucket_size

            if test_case.is_fail:

                failed_tests.append(test_case.test_name)
                stacktraces.append(test_case.fail_reasons)

                progress[bucket_idx+1] = s_symbol

            else:
                progress[bucket_idx+1] = f_symbol


            print(''.join(progress))

            if idx != self.total_tests-1:

                print(_LINE_UP, end=_LINE_CLEAR)
            

            if bucket_idx+1==bucket_size:
   
                for _ in range(len(previous_progress)):

                    print(_LINE_UP, end=_LINE_CLEAR)

                previous_progress.append(progress)

       
                for _ in range(len(previous_progress)):
                    print(''.join(previous_progress[_]))

                progress = ['[']+[e_symbol for _ in range(bucket_size)]+[']']
            
             
        time_taken = perf_counter() - start_timer
        errors = len(failed_tests)

        if self.mode == Mode.SUPER_MINIMAL:
            return errors, time_taken
        
        print('\nFinished running tests for < %s >\n' % (self.file_name, ))
        print('Tests passed: [ %d / %d ] (%0.4f) secs\n' 
            % (self.total_tests - errors, self.total_tests, time_taken, ))
        
        if not failed_tests:
            print('...\n')
            return errors, time_taken
        
        if self.mode == Mode.MINIMAL_NO_STACK:

            print('\nErrors:')

            for failed_test in failed_tests:
                print('\t—› %s' % (failed_test, ))

            print('...\n')
            return errors, time_taken
        
        idx = 0
        for test, traces in zip(failed_tests, stacktraces):
            idx += 1
            print('\nTEST\t—›  %s\n\t——› %s\n' % (self.module_name, test, ))

            for trace in traces:

                print(trace)

                if idx != errors:
                    print('%s ~~~ %s' % (Color.RED.value, _RESET, ))
    
        print('...\n')
        return errors, time_taken

    def run_tests(self) -> TestSuiteResults:
        
        _start = perf_counter()
        errors = 0

        print('Running tests for < %s >\n' % (self.file_name, ))

        self.populate_tests()
        self.box_tests()

        if self.mode == Mode.SORT:
            self.sort_tests()

        
        match self.mode:

            case Mode.NORMAL | Mode.SORT:
                errors, time_taken = self.show_test_results_non_minimal(start_timer=_start)

            case Mode.MINIMAL | Mode.MINIMAL_NO_STACK | Mode.SUPER_MINIMAL:
                errors, time_taken = self.show_test_results_minimal(start_timer=_start)
        

        print()
        return (time_taken, errors)
    
# TODO move @annotations
TestsContainer: TypeAlias = dict[str, dict[str, TestSuite]]
