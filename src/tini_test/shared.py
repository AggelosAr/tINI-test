from typing import Any, Callable, Optional

from tini_test._internals._registry import attach_state
from tini_test.misc.annotations import (MockDefinitionWrappedHolder,
                                        MockWrappedObject, RealTest,
                                        SharedDefinitionHolder,
                                        SharedWrappedObject, TestWrappedHolder,
                                        TestWrappedObject)
from tini_test.misc.exceptions import SharedOnlyAcceptsArguments


class SharedVar:

    def __init__(self, name: str):
        self.name = name



class Shared:

    def __new__(cls, *args: tuple[Any], **kwargs: Any):

        if kwargs:
            raise SharedOnlyAcceptsArguments

        return Shared.shared(*args)

    @classmethod
    def shared(cls,
               func: None
                   | RealTest 

                   | TestWrappedObject
                   | MockWrappedObject
                   | SharedWrappedObject

                   | TestWrappedHolder
                   | MockDefinitionWrappedHolder
                   | SharedDefinitionHolder = None,
                
               *args: Optional[tuple[Any]]

               ) ->  Callable[..., 
                              Callable[..., 
                                       SharedDefinitionHolder[SharedVar]]]:
        
        _vars = args

        def wrapper(func) ->  Callable[..., 
                                       SharedDefinitionHolder[SharedVar]]:

            def _wrapper(*args, **kwargs) -> SharedDefinitionHolder[SharedVar]:

                if _vars:
                    return _vars
                
                return func


            _shared_reg, _conn_reg = attach_state(func.__globals__, _wrapper.__globals__, mode='shared')
            
            if _conn_reg is None:
                return wrapper
            
            assert hex(id(_wrapper)) not in _shared_reg
            assert hex(id(_wrapper)) not in _conn_reg

            _shared_reg[hex(id(_wrapper))] = _wrapper
            _conn_reg[hex(id(_wrapper))] = hex(id(func))
            
            return _wrapper

        if callable(func):
            return wrapper(func)

        return wrapper
