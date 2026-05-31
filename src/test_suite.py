import importlib
import types
from functools import cached_property, partial
from typing import Callable, Optional, TypeAlias

from src.enums import Config, Mode
from src.misc.annotations import PartialObject
from src.misc.exceptions import NotSupportedMode
from src.test_utils import Test


class TestSuite:
    
    def __init__(self, 
                 module: str,
                 file: str,
                 mode: Optional[Mode | str] = Mode.SORT) -> None:
        
        if mode is None:
            mode = Mode.SORT

        match mode:
            case Mode.NORMAL:
                self.mode = Mode.NORMAL
            case Mode.NORMAL.value:
                self.mode = Mode.NORMAL
            case Mode.SORT:
                self.mode = Mode.SORT
            case Mode.SORT.value:
                self.mode = Mode.SORT
            case Mode.MINIMAL:
                self.mode = Mode.MINIMAL
            case Mode.MINIMAL.value:
                self.mode = Mode.MINIMAL
            case Mode.MINIMAL_NO_STACK:
                self.mode = Mode.MINIMAL_NO_STACK
            case Mode.MINIMAL_NO_STACK.value:
                self.mode = Mode.MINIMAL_NO_STACK
            case _:
                raise NotSupportedMode(msg=Mode.supported_modes())

        self.module = importlib.import_module('%s.%s' % (module, file, ))

        self.decorated_tests: list[Callable] = []

        self.collector: dict[str, Test] = dict()

    @cached_property
    def total_tests(self) -> int:
        return len(self.collector.values())

    @cached_property
    def file_name(self) -> str:
        return self.module.__name__
    
    def gather_tests(self, func_name: str) -> list[str]:

        tests = []

        for obj in dir(self.module):

            g_obj = getattr(self.module, obj)
            
            if not all([isinstance(g_obj, types.FunctionType), 
                        # TODO remove this 
                        hasattr(g_obj, '_xyz_is_a_test_case_uwu')]):
                continue 
            
            f_name = g_obj.__closure__[-1].cell_contents.__name__
            if func_name and f_name != func_name:
                continue
            
            tests.append(f_name)

            # TODO fix this XXX
            test_obj = partial(g_obj, _Test____collector=self.collector)
            self.decorated_tests.append(test_obj)

        return tests
    
    def populate_tests(self) -> None:
        list(map(lambda l: l(), self.decorated_tests))
    
    def sort_tests(self) -> None:
        self.collector = dict(sorted(self.collector.items(), 
                                     key=lambda kv: kv[1].is_fail))
        
    def box_tests(self) -> None:
        list(map(lambda l: l.box_test(), self.collector.values()))
    
    # TODO refactor to show_test_result
    def show_test_results(self, verbocity: Optional[bool] = True) -> None:
        
        print('Running tests for < %s >\n' % (self.file_name, ))

        minimal = list('[%s]' % (' '*self.total_tests, ))
        failed_tests = []
        stacktraces = []

        for idx, test_case in enumerate(self.collector.values(), start=1):
            
            match verbocity:

                case True:

                    print(str(test_case) % (idx, self.total_tests, ))

                    if test_case.is_fail:
                        failed_tests.append(test_case.test_name)

                case False:

                    match test_case.is_fail:

                        case True:
                            failed_tests.append(test_case.test_name)
                            stacktraces.append(test_case.fail_reasons)
                            minimal[idx] = ('%s . %s' 
                                            % (Config.RED.value, Config.RESET.value, ))

                        case False:
                            minimal[idx] = ('%s . %s' 
                                            % (Config.GREEN.value, Config.RESET.value, ))

                    print('%s' % ''.join(minimal))
                    
                    if idx != self.total_tests:
                        print(Config.LINE_UP.value, end=Config.LINE_CLEAR.value)

        print('\nTests passed: [ %d / %d ]' 
              % (self.total_tests - len(failed_tests), self.total_tests, ))

        if self.mode in {Mode.MINIMAL, Mode.MINIMAL_NO_STACK} and failed_tests:

            print('Failed tests: %s\n' % failed_tests)

            for test, traces in zip(failed_tests, stacktraces):
                
                if self.mode == Mode.MINIMAL_NO_STACK:
                    ...
                else:
                    print('TEST : %s' % (test, ))
                    for trace in traces:
                        print(trace)

        print()

    def run_tests(self) -> None:

        self.populate_tests()
        self.box_tests()

        match self.mode:

            case Mode.NORMAL:
                self.show_test_results()

            case Mode.SORT:
                self.sort_tests()
                self.show_test_results()

            case Mode.MINIMAL | Mode.MINIMAL_NO_STACK:
                self.show_test_results(verbocity=False)


# TODO move @annotations
TestsContainer: TypeAlias = dict[str, dict[str, TestSuite]]
