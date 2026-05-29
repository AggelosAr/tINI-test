import importlib
import io
import traceback
import types
from contextlib import redirect_stdout
from functools import cached_property, partial
from typing import Any, Callable, Optional

from src.enums import Config, Mode, TestStatus
from src.misc.annotations import F_Callable, S_Callable


class OperationState:

    def __init__(self, 
                 status: TestStatus,
                 redirected_output: Optional[io.StringIO] = io.StringIO(''),
                 detail: Optional[str] = '',
                 exception_trace: Optional[str] = ''):
        
        self.status = status

        self.redirected_output = redirected_output

        self.detail = self.format_detail(detail=detail)
        self.exception_trace = exception_trace

    def __str__(self) -> str:
        return '\n'.join(filter(lambda l: l != str(), # type: ignore[arg-type]
                                [
                                    self.inner_state,
                                    self.exception_trace,
                                    self.detail
                                ])
                        )
                            
    def __repr__(self) -> str:
        raise NotImplementedError
    
    @property
    def inner_state(self) -> str:
        return self.redirected_output.getvalue() # type: ignore[union-attr]
    
    def format_detail(self, 
                      indent: Optional[int] = 2,
                      detail: Optional[str] = '') -> str:

        pad = (lambda lvl: '\t'*lvl)(indent) # type: ignore[operator]

        match self.status:
            # (**1**)
            case TestStatus.SUCCESS:
                return '\n%s%s--------- [PASS] ---------%s' % (pad, Config.GREEN.value, Config.RESET.value)
            
            case TestStatus.FAIL:

                s_msg = ('%s%s*** EXCEPTION DURING TEST <%s> ***%s' 
                        % ( pad, Config.RED.value, detail, Config.RESET.value, ))
                e_msg = ('\n%s%s--------- [FAIL] ---------%s' 
                        % (pad, Config.RED.value, Config.RESET.value))
                
                return '%s\n%s' % (s_msg, e_msg)
        
        
            case TestStatus.SET_UP_SUCCESS:
                return '%s%s[*] Set up succeeded%s\n' % (pad, Config.BLUE.value, Config.RESET.value)
            
            case TestStatus.SET_UP_FAIL:

                s_msg = ('%s%s[*] Skipping test since set up failed.\n\t%sReason: %s%s' 
                        % (pad, Config.YELLOW.value, pad, detail, Config.RESET.value, ))
            
                e_msg = '\n%s%s------ [SET UP FAILED] ------%s' % (pad, Config.YELLOW.value, Config.RESET.value)

                t_msg = ('\n%s%s --------- [FAIL] ---------%s' 
                        % (pad, Config.RED.value, Config.RESET.value))
                
                return '%s\n%s\n%s' % (s_msg, e_msg, t_msg, )
        

            case TestStatus.BREAK_DOWN_SUCCESS:
                return '%s%s[*] Break down succeeded%s' % (pad, Config.BLUE.value, Config.RESET.value)
            
            case TestStatus.BREAK_DOWN_FAIL:
                s_msg = ('%s%s[*] Cleaning up failed.\n\t%sReason: %s%s' % 
                        (pad, Config.YELLOW.value, pad, detail, Config.RESET.value, ))
                
                e_msg = '\n%s%s------ [BREAK DOWN FAILED] ------%s' % (pad, Config.YELLOW.value, Config.RESET.value)

                t_msg = ('\n%s%s  --------- [FAIL] ---------%s' 
                        % (pad, Config.RED.value, Config.RESET.value))
                
                return '%s\n%s\n%s' % (s_msg, e_msg, t_msg, )

            case TestStatus.NO_OP:
                return ''


class TestStep:

    def __init__(self,
                 func,
                 success_status,
                 fail_status,
                 args: Optional[tuple] = (),
                 kwargs: Optional[dict[str, Any]] = {}) -> None:

        self.func = func
        self.args = args
        self.kwargs = kwargs

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
            return OperationState(status=self.fail_status,
                                  redirected_output=buffer,
                                  detail=str(e),
                                  exception_trace=exception_trace)
        
        return OperationState(status=self.success_status,
                              redirected_output=buffer)


class Test:

    def __init__(self,
                 test: F_Callable, 
                 test_args: tuple,
                 test_kwargs: dict[str, Any],
                 setup: Optional[S_Callable] = None, 
                 cleanup: Optional[S_Callable] = None) -> None:

        self.test_name = test.__name__

        self.steps = [
            TestStep(func=cleanup,
                     success_status=TestStatus.BREAK_DOWN_SUCCESS,
                     fail_status=TestStatus.BREAK_DOWN_FAIL),
            TestStep(func=test,
                     args=test_args,
                     kwargs=test_kwargs,
                     # (**1**) 
                     # We will use no op here
                     # Since the print order is not the 
                     # same as the excecution order...
                     # success_status=TestStatus.SUCCESS,
                     # fail_status=TestStatus.FAIL),
                     success_status=TestStatus.NO_OP,
                     fail_status=TestStatus.NO_OP),
            TestStep(func=setup,
                     success_status=TestStatus.SET_UP_SUCCESS,
                     fail_status=TestStatus.SET_UP_FAIL)
        ]
    
        self.operations: list[OperationState] = []
    
    def __str__(self) -> str:
        test = []
        # Placeholder for test enumeration kinda bad...
        test.append('[ %%s / %%s ] %s%s< %s >\n' 
                    % ('\t', '\t', self.test_name, ))

        test.extend(filter(lambda l: l != str(), map(str, self.operations)))
        
        return '\n'.join(test)

    def __repr__(self) -> str:
        raise NotImplementedError
    
    @classmethod
    def case(cls,
             test_func: Optional[F_Callable] = None,
             *, 
             setup: Optional[S_Callable] = None, 
             cleanup: Optional[S_Callable] = None) -> F_Callable:

        def wrapper(test_func: F_Callable):
            
            def _wrapper(*args, ____collector, **kwargs) -> Any:
                
                test_case = Test(test=test_func,
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
    
    def box_test(self) -> list[OperationState]:
        
        while self.steps:

            step_state = self.steps.pop().run_step()
            self.operations.append(step_state)

            if TestStatus.is_abort_cause(status=step_state.status):
                break
              
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
            case _:
                raise Exception(Mode.supported_modes())
            
        try:
            self.module = importlib.import_module(module)
        except Exception as e:
            print('Failed to initialize tests <%s>' % (str(e), ))
            raise

        # list of decorated tests
        self.d_to_tests: list[Callable] = []

        self.collector: dict[str, Test] = dict()

    @property
    def total_tests(self) -> int:
        return len(self.collector.values())
    
    @cached_property
    def seperator(self) -> str:

        match self.mode:

            case Mode.NORMAL | Mode.SORT:
                return '\n%s%s%s%s\n' % (Config.NEGATIVE.value, Config.CYAN.value, 120*'=', Config.RESET.value, )
            
            case Mode.MINIMAL:
                return '\n'
            
            case _:
                raise NotImplementedError

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

            p_obj = partial(obj_v, _Test____collector=self.collector)
            self.d_to_tests.append(p_obj)
    
    def populate_tests(self) -> None:
        list(map(lambda l: l(), self.d_to_tests))
    
    def sort_tests(self) -> None:
        # TODO maybe sort tests first by setp fails and then by actual fails?
        self.collector = dict(sorted(self.collector.items(), 
                                     key=lambda kv: kv[1].is_fail))
        
    def box_tests(self) -> None:
        list(map(lambda l: l.box_test(), self.collector.values()))
    
    def show_test_results(self, verbocity: Optional[bool] = True) -> None:
        
        print('Running tests for < %s >\n' % (self.file_name, ))
        print(self.seperator)

        minimal = list('[%s]' % (' '*self.total_tests, ))
        failed_tests = []

        for idx, test_case in enumerate(self.collector.values(), start=1):
            
            match verbocity:

                case True:
                    print(str(test_case) % (idx, self.total_tests, ))

                    match test_case.is_fail:
                        case True:
                            failed_tests.append(test_case.test_name)
                        case False:
                            # (**1**)
                            print(OperationState(status=TestStatus.SUCCESS))

                    print(self.seperator)

                case False:

                    match test_case.is_fail:
                        case True:
                            failed_tests.append(test_case.test_name)
                            minimal[idx] = '%s . %s' % (Config.RED.value, Config.RESET.value, )
                        case False:
                            minimal[idx] = '%s . %s' % (Config.GREEN.value, Config.RESET.value, )

                    print('%s' % ''.join(minimal))
                    
                    if idx != self.total_tests:
                        print(Config.LINE_UP.value, end=Config.LINE_CLEAR.value)

   
        print('\nTests passed: [ %d / %d ]' 
              % (self.total_tests - len(failed_tests), self.total_tests, ))
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
            case Mode.MINIMAL:
                self.show_test_results(verbocity=False)
