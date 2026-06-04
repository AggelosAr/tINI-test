from functools import partial
from importlib import import_module
from time import perf_counter
from types import FunctionType
from typing import Callable, Optional, TypeAlias

from ._internals.consts import _LINE_CLEAR, _LINE_UP, _RESET
from .enums import Color, Mode
from .misc.annotations import Errors, TestName, TestSuiteResults
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
        list(map(lambda l: l.box_test(), self.collector.values()))
    
    def show_test_results_non_minimal(self) -> Errors:

        failed_tests = 0

        for idx, test_case in enumerate(self.collector.values(), start=1):

            print("[ %s / %s ] TEST: < %s >\n%s" 
                  % (idx, self.total_tests, test_case.test_name, str(test_case)))
           
            failed_tests += test_case.is_fail

        return failed_tests

    def show_test_results_minimal(self) -> Errors:

        minimal = list('[%s]' % (' '*self.total_tests, ))
        failed_tests = []
        stacktraces = []

        for idx, test_case in enumerate(self.collector.values(), start=1):
        
            if test_case.is_fail:

                failed_tests.append(test_case.test_name)
                stacktraces.append(test_case.fail_reasons)
                minimal[idx] = ('%s . %s' % (Color.RED.value, _RESET, ))

            else:
                minimal[idx] = ('%s . %s' % (Color.GREEN.value, _RESET, ))

            print('%s' % ''.join(minimal))
            
            if idx != self.total_tests:
                print(_LINE_UP, end=_LINE_CLEAR)

        if not failed_tests:
            return len(failed_tests)
        
        if self.mode == Mode.MINIMAL_NO_STACK:
            return len(failed_tests)
        
        if self.mode == Mode.SUPER_MINIMAL:
            return len(failed_tests)
        
        for test, traces in zip(failed_tests, stacktraces):
            
            print('TEST : %s' % (test, ))
            for trace in traces:
                print('...')
                print(trace)
                print('...')

        return len(failed_tests)

    def run_tests(self) -> TestSuiteResults:
        
        _start = perf_counter()

        print('Running tests for < %s >\n' % (self.file_name, ))

        self.populate_tests()
        self.box_tests()

        if self.mode == Mode.SORT:
            self.sort_tests()

        errors = 0

        match self.mode:

            case Mode.NORMAL | Mode.SORT:
                errors += self.show_test_results_non_minimal()

            case Mode.MINIMAL | Mode.MINIMAL_NO_STACK | Mode.SUPER_MINIMAL:
                errors += self.show_test_results_minimal()
        
        time_taken = perf_counter() - _start

        if self.mode != Mode.SUPER_MINIMAL:
            
            print('Finished running tests for < %s >\n' % (self.file_name, ))

            print('Tests passed: [ %d / %d ] (%f) secs\n' 
                % (self.total_tests - errors, self.total_tests, time_taken, ))

            print('...\n')

        print()
        return (time_taken, errors)
    
# TODO move @annotations
TestsContainer: TypeAlias = dict[str, dict[str, TestSuite]]
