from contextlib import redirect_stdout
from functools import cached_property
from io import StringIO
from traceback import format_exc, format_tb
from typing import Any, Optional

from src._internals._internal_exceptions._exceptions import (
    _FailStateWasNotFail, _LastOpNotExpected)
from src.enums import Config, TestStatus
from src.misc.annotations import F_Callable, S_Callable, StackTrace
from src.misc.exceptions import ExpectedWasDifferentFromActual
from src.state.state import OperationState


class TestStep:

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

        buffer = StringIO()

        try:
            with redirect_stdout(buffer):
                self.func(*self.args, **self.kwargs)

        except ExpectedWasDifferentFromActual as e:
           
            exception_trace = '\n'.join(format_tb(e.__traceback__))
            
            return OperationState(entry_status=self.entry_status,
                                  status=self.fail_status,
                                  detail=str(e),
                                  exception_trace=exception_trace,
                                  redirected_output=buffer)

        except Exception as e:
            exception_trace = format_exc()
            return OperationState(entry_status=self.entry_status,
                                  status=self.fail_status,
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

        self.test = test

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
    
        self.operation_states: list[OperationState] = []
    
    def __str__(self) -> str:
        return '\n'.join(filter(lambda l: l != str(), map(str, self.operation_states)))

    def __repr__(self) -> str:
        raise NotImplementedError
    
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
        return any(TestStatus.is_fail_cause(op.status) for op in self.operation_states)
    
    @property
    def test_name(self) -> str:
        return self.test.__name__
    
    @property
    def fail_state(self) -> TestStatus:
        return self._fail_state

    @fail_state.setter
    def fail_state(self, new_state: TestStatus) -> None:
        assert TestStatus.is_fail_cause(new_state), _FailStateWasNotFail
        self._fail_state = new_state

    @property
    def fail_reasons(self) -> list[StackTrace]:
        return self._fail_reasons

    @fail_reasons.setter
    def fail_reasons(self, reason: StackTrace) -> None:
        self._fail_reasons.append(reason)

    def run_steps(self) -> None:
        
        while self.steps:

            step_state = self.steps.pop().run_step()
            self.operation_states.append(step_state)
            
            if TestStatus.is_fail_cause(status=step_state.status):
                self.fail_state = step_state.status
                self.fail_reasons.append(step_state.exception_trace)
                break
    
    def run_for_cleanup_if_needed(self) -> None:
        # TODO What happens if user stops the program?
        # If test fails and there is a cleanup 
        # Attempt to run it
        
        if not (self.is_fail and self.steps and self.steps[0].func):
            return 

        # There are two cases either the test failed on setup or on main
        cleanup_step = self.steps[0]
        failed_op = self.operation_states.pop()
        
        match failed_op.status:
            case TestStatus.SET_UP_FAIL:
                cleanup_step.entry_status=TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_SETUP_FAIL
            case TestStatus.FAIL:
                # Modify the failed_op status for visual purposes
                failed_op.status = TestStatus.NO_OP
                cleanup_step.entry_status=TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_FAIL
            case _:
                raise _LastOpNotExpected
            
        cleanup_step.success_status=TestStatus.ATTEMPT_BREAK_DOWN_SUCCESS
        cleanup_step.fail_status=TestStatus.ATTEMPT_BREAK_DOWN_FAIL
        
        cleanup_op = cleanup_step.run_step()

        # Put back the states in the correct order
        self.operation_states.append(failed_op)
        self.operation_states.append(cleanup_op)

        if TestStatus.is_fail_cause(status=cleanup_op.status):
            self.fail_state = cleanup_op.status
            self.fail_reasons.append(cleanup_op.exception_trace)
        
    def attach_end_state(self) -> None:
        
        match self.is_fail:

            case True:
                if self.operation_states[-1].status != TestStatus.FAIL:
                    fail_op = OperationState(TestStatus.FAIL)
                    self.operation_states.append(fail_op)
            
            case False:
                success_op = OperationState(TestStatus.SUCCESS)
                self.operation_states.append(success_op)

    def align_message(self, el: str) -> str:
        return '%s%s' % ((Config.SEPERATOR_LENGTH.value // 2 - (len(el) // 2)) * str(' '), el, )

    # TODO align messages relative to each other also 
    def align_messages(self) -> None:

        for op in self.operation_states:
            op.entry_msg = list(map(self.align_message, op.entry_msg))
            op.exit_msg = list(map(self.align_message, op.exit_msg))

    def close_state(self) -> None:
        end_state = OperationState(TestStatus.NO_OP) # fishy maybe add another state
        end_state.exit_msg = OperationState.get_end_seperator()
        self.operation_states.append(end_state)

    def box_test(self) -> list[OperationState]:

        self.run_steps()
        self.run_for_cleanup_if_needed()
        self.attach_end_state()
        self.align_messages()
        self.close_state()
        
        #!
        if self._no_op:
            with redirect_stdout(StringIO()):
                self._no_op.__call__()

        return self.operation_states
