from functools import partial
from importlib import import_module
from time import perf_counter
from types import FunctionType
from typing import Callable, Optional, TypeAlias

from small_test._internals.consts import _LINE_CLEAR, _LINE_UP, _RESET
from small_test.enums import Color, Mode
from small_test.misc.annotations import Failures, TestName, TestSuiteResults
from small_test.misc.exceptions import NotSupportedMode
from small_test.test_utils import Test

_MINIMALS = {Mode.MINIMAL, Mode.MINIMAL_NO_STACK, Mode.SUPER_MINIMAL}


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
                        # TODO remove this 
                        hasattr(g_obj, '_xyz_is_a_test_case_uwu')]):
                continue 
            
            test_name = str(g_obj.__closure__[-1].cell_contents.__name__)  # TODO xxx
            if func_name and test_name != func_name:
                continue
            
            test_names.append(test_name)

            # TODO fix this XXX
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
    
    # TODO refactor to show_test_result !!!
    def show_test_results(self, verbocity: Optional[bool] = True) -> Failures:
        
        if self.mode != Mode.SUPER_MINIMAL:
            print('Running tests for < %s >\n' % (self.file_name, ))

        minimal = list('[%s]' % (' '*self.total_tests, ))
        failed_tests = []
        stacktraces = []

        for idx, test_case in enumerate(self.collector.values(), start=1):
            
            match verbocity:

                case True:
                    
                    print("[ %s / %s ] TEST: < %s >\n" % (idx, self.total_tests, test_case.test_name))
                    print(str(test_case))
                    
                    if test_case.is_fail:
                        failed_tests.append(test_case.test_name)

                case False:

                    match test_case.is_fail:

                        case True:
                            failed_tests.append(test_case.test_name)
                            stacktraces.append(test_case.fail_reasons)
                            minimal[idx] = ('%s . %s' 
                                            % (Color.RED.value, _RESET, ))

                        case False:
                            minimal[idx] = ('%s . %s' 
                                            % (Color.GREEN.value, _RESET, ))

                    print('%s' % ''.join(minimal))
                    
                    if idx != self.total_tests:
                        print(_LINE_UP, end=_LINE_CLEAR)

        print('\nTests passed: [ %d / %d ]' 
              % (self.total_tests - len(failed_tests), self.total_tests, ))


        if self.mode in _MINIMALS and failed_tests:
            
            if self.mode == Mode.SUPER_MINIMAL:
                return len(failed_tests)
            
            print('Failed tests: %s\n' % failed_tests)

            for test, traces in zip(failed_tests, stacktraces):
                
                if self.mode == Mode.MINIMAL_NO_STACK:
                    ...
                else:
                    print('TEST : %s' % (test, ))
                    for trace in traces:
                        print(trace)

        print()

        return len(failed_tests)

    def run_tests(self) -> TestSuiteResults:
        
        _start = perf_counter()

        self.populate_tests()
        self.box_tests()

        failures = 0

        match self.mode:

            case Mode.NORMAL:
                failures += self.show_test_results()

            case Mode.SORT:
                self.sort_tests()
                failures += self.show_test_results()

            case Mode.MINIMAL | Mode.MINIMAL_NO_STACK | Mode.SUPER_MINIMAL:
                failures += self.show_test_results(verbocity=False)

        return (perf_counter() - _start, failures)
    
# TODO move @annotations
TestsContainer: TypeAlias = dict[str, dict[str, TestSuite]]
