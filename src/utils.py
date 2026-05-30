import importlib
import io
import traceback
import types
from contextlib import redirect_stdout
from functools import cached_property, partial
from typing import Any, Callable, Optional

from src.enums import Config, Mode, TestStatus
from src.misc.annotations import F_Callable, S_Callable, StackTrace
from src.misc.exceptions import LastOpNotExpected
from src.state import OperationState


class TestStep:

    # TODO maybe add exit status here? Will this make our lives easier?
    def __init__(self,
                 func: F_Callable | S_Callable | None,
                 success_status: TestStatus,
                 fail_status: TestStatus,
                 entry_status: Optional[TestStatus] = TestStatus.NO_OP,
                 args: Optional[tuple] = (),
                 kwargs: Optional[dict[str, Any]] = {}) -> None:

        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.entry_status = entry_status
        self.success_status = success_status
        self.fail_status = fail_status

    def run_step(self):
        
        if self.func is None:
            return OperationState(status=TestStatus.NO_OP)

        buffer = io.StringIO()

        try:
            with redirect_stdout(buffer):
                self.func(*self.args, **self.kwargs)
        except Exception as e:
            exception_trace = traceback.format_exc()
            return OperationState(entry_status=self.entry_status,
                                  status=self.fail_status,
                                  detail=str(e),
                                  redirected_output=buffer,
                                  exception_trace=exception_trace)
        
        return OperationState(entry_status=self.entry_status,
                              status=self.success_status,
                              redirected_output=buffer)


class Test:

    def __init__(self,
                 args,
                 /,
                 test: F_Callable, 
                 test_args: tuple,
                 test_kwargs: dict[str, Any],
                 setup: Optional[S_Callable] = None, 
                 cleanup: Optional[S_Callable] = None) -> None:

        self.test_name = test.__name__

        self._no_op = args

        self._fail_state = TestStatus.NO_OP
        self._fail_reasons: list[StackTrace] = []

        self.steps = [
            TestStep(func=cleanup,
                     entry_status=TestStatus.BREAK_DOWN_ENTRY,
                     success_status=TestStatus.BREAK_DOWN_SUCCESS,
                     fail_status=TestStatus.BREAK_DOWN_FAIL),
            TestStep(func=test,
                     args=test_args,
                     kwargs=test_kwargs,
                     success_status=TestStatus.NO_OP,
                     fail_status=TestStatus.FAIL),
            TestStep(func=setup,
                     entry_status=TestStatus.SET_UP_ENTRY,
                     success_status=TestStatus.SET_UP_SUCCESS,
                     fail_status=TestStatus.SET_UP_FAIL)
        ]
    
        self.operations: list[OperationState] = []
    
    def __str__(self) -> str:
        test = []
        # Placeholder for test enumeration
        test.append('[ %%s / %%s ] %s%s< %s >\n' 
                    % ('\t', '\t', self.test_name, ))

        test.extend(filter(lambda l: l != str(), map(str, self.operations)))
        
        return '\n'.join(test)

    def __repr__(self) -> str:
        raise NotImplementedError
    
    # TODO fix this XXX
    @classmethod
    def case(cls,
             test_func: Optional[F_Callable] = None,
             *,
             setup: Optional[S_Callable] = None, 
             cleanup: Optional[S_Callable] = None,
             _no_op: Optional[S_Callable] = None) -> F_Callable:
        
        def wrapper(test_func: F_Callable):
            
            def _wrapper(*args, ____collector, **kwargs) -> Any:

                test_case = Test(_no_op,
                                 test=test_func,
                                 test_args=args,
                                 test_kwargs=kwargs,
                                 setup=setup,
                                 cleanup=cleanup)

                ____collector[test_func.__name__] = test_case

            _wrapper._xyz_is_a_test_case_uwu = True # type: ignore[attr-defined]

            return _wrapper

        if test_func is None:
            return wrapper
        else:
            return wrapper(test_func)
    
    @cached_property
    def is_fail(self) -> bool:
        return any(TestStatus.is_abort_cause(op.status) for op in self.operations)
    
    @property
    def fail_state(self) -> TestStatus:
        return self._fail_state

    @fail_state.setter
    def fail_state(self, new_state: TestStatus) -> None:
        # TODO assert new_state is indeed fail state
        self._fail_state = new_state

    @property
    def fail_reasons(self) -> list[StackTrace]:
        return self._fail_reasons

    @fail_reasons.setter
    def fail_reasons(self, reason: StackTrace) -> None:
        self._fail_reasons.append(reason)

    def run_steps(self) -> None:
        
        while self.steps:

            test_step = self.steps.pop().run_step()
            self.operations.append(test_step)
            
            if TestStatus.is_abort_cause(status=test_step.status):
                self.fail_state = test_step.status
                self.fail_reasons.append(test_step.exception_trace)
                break
    
    def run_for_cleanup_if_needed(self) -> None:
        # What happens if user stops the program?
        # If test fails and there is a cleanup 
        # Attempt to run it
        
        if not (self.is_fail and self.steps and self.steps[0].func):
            return 

        cleanup = self.steps[0]
        last_op = self.operations.pop()
        
        match last_op.status:
            case TestStatus.SET_UP_FAIL:
                cleanup.entry_status=TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_SETUP_FAIL
            case TestStatus.FAIL:
                # Modify the last_op for visual purposes
                last_op.status = TestStatus.NO_OP
                cleanup.entry_status=TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_FAIL
            case _:
                raise LastOpNotExpected
            
        cleanup.success_status=TestStatus.ATTEMPT_BREAK_DOWN_SUCCESS
        cleanup.fail_status=TestStatus.ATTEMPT_BREAK_DOWN_FAIL
        
        test_step = cleanup.run_step()

        self.operations.append(last_op)
        self.operations.append(test_step)

        if TestStatus.is_fail_cause(status=test_step.status):
            self.fail_state = test_step.status
            self.fail_reasons.append(test_step.exception_trace)
        
    def attach_end_seperator(self) -> None:
        
        match self.is_fail:

            case True:
                if self.operations[-1].status != TestStatus.FAIL:
                    fail_op = OperationState(TestStatus.FAIL)
                    self.operations.append(fail_op)
            
            case False:
                success_op = OperationState(TestStatus.SUCCESS)
                self.operations.append(success_op)

    def box_test(self) -> list[OperationState]:

        self.run_steps()
        self.run_for_cleanup_if_needed()
        self.attach_end_seperator()

        #!
        if self._no_op:
            with redirect_stdout(io.StringIO()):
                self._no_op.__call__()

        return self.operations

class ModuleTests:
    
    def __init__(self, 
                 module: str, 
                 mode: Optional[Mode | str] = Mode.SORT) -> None:
        
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
                raise Exception(Mode.supported_modes())

        self.module = importlib.import_module(module)

        # list of decorated tests
        self.d_to_tests: list[Callable] = []

        self.collector: dict[str, Test] = dict()

    @cached_property
    def total_tests(self) -> int:
        return len(self.collector.values())

    @cached_property
    def file_name(self) -> str:
        return self.module.__name__
    
    def gather_tests(self) -> None:
        
        for obj in dir(self.module):

            obj_v = getattr(self.module, obj)

            if not all([isinstance(obj_v, types.FunctionType), 
                        # TODO remove this 
                        hasattr(obj_v, '_xyz_is_a_test_case_uwu')]):
                continue 
            
            # TODO fix this XXX
            p_obj = partial(obj_v, _Test____collector=self.collector)
            self.d_to_tests.append(p_obj)
    
    def populate_tests(self) -> None:
        list(map(lambda l: l(), self.d_to_tests))
    
    def sort_tests(self) -> None:
        self.collector = dict(sorted(self.collector.items(), 
                                     key=lambda kv: kv[1].is_fail))
        
    def box_tests(self) -> None:
        list(map(lambda l: l.box_test(), self.collector.values()))
    
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
                            minimal[idx] = '%s . %s' % (Config.RED.value, Config.RESET.value, )

                        case False:
                            minimal[idx] = '%s . %s' % (Config.GREEN.value, Config.RESET.value, )

                    print('%s' % ''.join(minimal))
                    
                    if idx != self.total_tests:
                        print(Config.LINE_UP.value, end=Config.LINE_CLEAR.value)

        print('\nTests passed: [ %d / %d ]' 
              % (self.total_tests - len(failed_tests), self.total_tests, ))

        if not verbocity and failed_tests:

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
