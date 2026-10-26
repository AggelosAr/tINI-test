from typing import Any, Callable

from tini_test._internals._registry import attach_state
from tini_test.enums import Plugs
from tini_test.misc.annotations import (IsolateWrappedObject,
                                        MockDefinitionWrappedHolder,
                                        MockWrappedObject, RealTest,
                                        SharedDefinitionHolder,
                                        SharedWrappedObject, TestWrappedHolder,
                                        TestWrappedObject, WrapperInput)


class Isolate:
    '''
    The `@Isolate` decorator can be used to isolate the execution of test cases.

    This ensures that the state of the function or test case is separated from the
    global state, preventing side effects from affecting other parts of the code.

    It is enabled by default when the test case includes the 
    `@Mock` or `@Shared` decorators.
    '''
    def __new__(cls, *args: tuple[Any], **kwargs: Any):

        if kwargs:
            raise RuntimeError('Isolate does not accept keyword arguments')

        return _XIsolate.isolate(*args)


class _XIsolate:

    @staticmethod
    def isolate(func: None
                      | RealTest 

                      | TestWrappedObject
                      | MockWrappedObject
                      | SharedWrappedObject

                      | IsolateWrappedObject

                      | TestWrappedHolder
                      | MockDefinitionWrappedHolder
                      | SharedDefinitionHolder = None

                ) ->  Callable[..., 
                               Callable[..., 
                                        WrapperInput]]:

        def wrapper(func) ->  Callable:

            def _wrapper(*args, **kwargs) -> WrapperInput:

                return func
            
            _isol_reg, _conn_reg = attach_state(func.__globals__, _wrapper.__globals__, mode=Plugs.ISOLATE)

            if _isol_reg is None or _conn_reg is None:
                return wrapper
            
            assert hex(id(_wrapper)) not in _isol_reg
            assert hex(id(_wrapper)) not in _conn_reg

            _isol_reg[hex(id(_wrapper))] = _wrapper
            _conn_reg[hex(id(_wrapper))] = hex(id(func))
            
            return _wrapper

        if callable(func):
            return wrapper(func)
        
        return wrapper
