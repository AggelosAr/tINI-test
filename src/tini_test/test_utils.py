import asyncio
from collections import deque
from functools import cached_property
from io import StringIO
from traceback import format_exc, format_tb
from typing import Any, Callable, Mapping, Optional

from tini_test.context_managers import _thread_redirect_stdout

from .enums import TestStatus, Verbosity
from .misc.annotations import (F_Callable, MockWrappedObject, S_Callable,
                               StackTrace, TestWrappedObject)
from .misc.exceptions import ExpectedWasDifferentFromActual
from .mock import MockDefinition
from .state.state import OperationState

_minimals_discard = {Verbosity.MINIMAL_NO_STACK, Verbosity.SUPER_MINIMAL}


class TestStep:

    def __init__(self,
                 func: F_Callable | S_Callable | None,
                 success_status: TestStatus,
                 fail_status: TestStatus,
                 entry_status: Optional[TestStatus] = TestStatus.NO_OP,
                 args: Optional[tuple] = None,
                 kwargs: Optional[Mapping[str, Any]] = None,
                 mocks: Optional[list[MockDefinition]] = None) -> None:

        self.func = func
        self.args = args or ()
        self.kwargs = kwargs or {}

        self.mocks = mocks or []

        self.entry_status = entry_status
        self.success_status = success_status
        self.fail_status = fail_status

    def run_step(self, verbosity: Verbosity):
        
        if self.func is None:
            return OperationState(status=TestStatus.NO_OP)

        buffer = StringIO()

        apply_filters = verbosity in _minimals_discard

        try:
            # TODO add match on enum to discard output and exception traces in minimal modes
            with _thread_redirect_stdout(buffer):

                # TODO add a context manager here!
                deque(map(lambda mock: mock.patch(), self.mocks), maxlen=0)
                self.func(*self.args, **self.kwargs)
                deque(map(lambda mock: mock.restore(), self.mocks), maxlen=0)

        except ExpectedWasDifferentFromActual as e:

            deque(map(lambda mock: mock.restore(), self.mocks), maxlen=0)

            exception_trace = '\n'.join(format_tb(e.__traceback__))
            return OperationState(entry_status=self.entry_status,
                                  status=self.fail_status,
                                  detail=str(e) if not apply_filters else '',
                                  exception_trace=exception_trace if not apply_filters else '',
                                  redirected_output=buffer if not apply_filters else StringIO(''))

        except Exception as e:

            deque(map(lambda mock: mock.restore(), self.mocks), maxlen=0)

            exception_trace = format_exc()
            return OperationState(entry_status=self.entry_status,
                                  status=self.fail_status,
                                  redirected_output=buffer if not apply_filters else StringIO(''),
                                  exception_trace=exception_trace if not apply_filters else '')
        
        return OperationState(entry_status=self.entry_status,
                              status=self.success_status,
                              redirected_output=buffer if not apply_filters else StringIO(''))


class Test:

    def __init__(self,
                 args,
                 /,
                 verbosity: Verbosity,
                 test: F_Callable,
                 test_args: tuple,
                 test_kwargs: dict[str, Any],
                 setup: Optional[S_Callable] = None, 
                 cleanup: Optional[S_Callable] = None,
                 mocks: Optional[list[MockDefinition]] = None) -> None:

        self.verbosity = verbosity

        self.test = test

        self._no_op = args

        self.mocks = mocks or []

        self._fail_state = TestStatus.NO_OP
        self._fail_reasons: list[StackTrace] = []

        self.steps = [
            TestStep(func=cleanup,
                     mocks=mocks,
                     entry_status=TestStatus.BREAK_DOWN_ENTRY,
                     success_status=TestStatus.BREAK_DOWN_SUCCESS,
                     fail_status=TestStatus.BREAK_DOWN_FAIL),
            TestStep(func=test,
                     args=test_args,
                     kwargs=test_kwargs,
                     mocks=mocks,
                     success_status=TestStatus.NO_OP,
                     fail_status=TestStatus.FAIL),
            TestStep(func=setup,
                     mocks=mocks,
                     entry_status=TestStatus.SET_UP_ENTRY,
                     success_status=TestStatus.SET_UP_SUCCESS,
                     fail_status=TestStatus.SET_UP_FAIL)
        ]
    
        self.operation_states: list[OperationState] = []
    
    def __str__(self) -> str:
        return '\n'.join(filter(lambda l: l != str(), map(str, self.operation_states)))

    @classmethod
    def case(cls,
             test_func: None 
                        | Callable 
                        | MockWrappedObject
                        | TestWrappedObject = None,
             /,
             *args   : Any,
             setup   : Optional[F_Callable] = None,
             cleanup : Optional[F_Callable] = None,
             _no_op  : Optional[F_Callable] = None) -> F_Callable:
        
        
        def wrapper(test_func: F_Callable):
     

            def _wrapper(*args         : Any,
                         ____test_func : Optional[F_Callable] = test_func,
                         ____collector : dict[str, Test], 
                         ____verbosity : Verbosity,
                         ____mocks     : list[MockDefinition] = [],
                         **kwargs      : Any) -> Any:

                assert ____test_func
                
                test_case = Test(_no_op,
                                 test=____test_func,
                                 test_args=args,
                                 test_kwargs=kwargs,
                                 setup=setup,
                                 cleanup=cleanup,
                                 verbosity=____verbosity,
                                 mocks=____mocks)

                ____collector[____test_func.__name__ or test_func.__name__] = test_case
                return _wrapper

            _test_reg = test_func.__globals__.get('_TEST_REGISTRY')
            _conn_reg = test_func.__globals__.get('_CONN_REGISTRY')

            assert hex(id(_wrapper)) not in _test_reg
            assert hex(id(_wrapper)) not in _conn_reg

            _test_reg[hex(id(_wrapper))] = _wrapper
            _conn_reg[hex(id(_wrapper))] = hex(id(test_func))

            return _wrapper


        if callable(test_func) and not args and setup is None and cleanup is None and _no_op is None:
            r = wrapper(test_func)
        
            return r

        if test_func is not None:
            args = (test_func, *args)

        if len(args) > 0:
            setup = args[0]

        if len(args) > 1:
            cleanup = args[1]
        
        if len(args) > 2:
            _no_op = args[2]

        return wrapper
    
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
        self._fail_state = new_state

    @property
    def fail_reasons(self) -> list[StackTrace]:
        return self._fail_reasons

    @fail_reasons.setter
    def fail_reasons(self, reason: StackTrace) -> None:
        self._fail_reasons.append(reason)

    def run_steps(self, _verbosity: Optional[Verbosity] = None) -> None:
        
        while self.steps:

            step_state = self.steps.pop().run_step(self.verbosity)
            self.operation_states.append(step_state)
            
            if TestStatus.is_fail_cause(status=step_state.status):
                self.fail_state = step_state.status
                self.fail_reasons.append(step_state.exception_trace)
                break
    
    def run_for_cleanup_if_needed(self, _verbosity: Optional[Verbosity] = None) -> None:
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
            
        cleanup_step.success_status=TestStatus.ATTEMPT_BREAK_DOWN_SUCCESS
        cleanup_step.fail_status=TestStatus.ATTEMPT_BREAK_DOWN_FAIL
        
        cleanup_op = cleanup_step.run_step(self.verbosity)

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

    def close_state(self) -> None:
        end_state = OperationState(TestStatus.NO_OP) # fishy maybe add another state
        end_state.exit_msg = OperationState.get_end_seperator()
        self.operation_states.append(end_state)

    def box_test(self, _verbosity: Optional[Verbosity] = None) -> None:

        self.run_steps()
        self.run_for_cleanup_if_needed()
        self.attach_end_state()
        self.close_state()

        if self._no_op and callable(self._no_op):
            from contextlib import redirect_stdout

            with redirect_stdout(StringIO()):
                self._no_op.__call__()

    async def abox_test(self, _verbosity: Optional[Verbosity] = None) -> None:
        await asyncio.to_thread(self.box_test)
