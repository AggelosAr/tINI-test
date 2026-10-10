from typing import Any, Callable

from tini_test._internals._registry import attach_state
from tini_test.enums import Plugs
from tini_test.misc.annotations import (IsolateWrappedObject,
                                        MockDefinitionWrappedHolder,
                                        MockWrappedObject, RealTest,
                                        SharedDefinitionHolder,
                                        SharedWrappedObject, TestWrappedHolder,
                                        TestWrappedObject, WrapperInput)

# Experimental.

class Isolate:
    
    def __new__(cls, *args: tuple[Any], **kwargs: Any):

        if kwargs:
            raise RuntimeError('Isolate does not accept keyword arguments')

        return _XIsolate.isolate(*args)


class _XIsolate:

    @classmethod
    def isolate(cls,
                func: None
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

        def wrapper(func) ->  Callable[..., 
                                       WrapperInput]:

            def _wrapper(*args, **kwargs) -> WrapperInput:

                return func
            
            _isol_reg, _conn_reg = attach_state(func.__globals__, _wrapper.__globals__, mode=Plugs.ISOLATE)
            
            if _conn_reg is None:
                return wrapper
            
            assert hex(id(_wrapper)) not in _isol_reg
            assert hex(id(_wrapper)) not in _conn_reg

            _isol_reg[hex(id(_wrapper))] = _wrapper
            _conn_reg[hex(id(_wrapper))] = hex(id(func))
            
            return _wrapper

        if callable(func):
            return wrapper(func)
        
        return wrapper
