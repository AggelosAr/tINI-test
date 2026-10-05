from typing import Any, Callable, Optional

from tini_test._internals._registry import attach_state
from tini_test.misc.annotations import (MockDefinitionWrappedHolder,
                                        MockWrappedObject, RealTest,
                                        SharedDefinitionHolder,
                                        SharedWrappedObject, TestWrappedHolder,
                                        TestWrappedObject)
from tini_test.misc.exceptions import (SharedAcceptedInvalidArguments,
                                       SharedOnlyAcceptsArguments)


class NotInitialized:
    object


class SharedVar:

    def __new__(cls, name: str) -> 'SharedVar':
        instance = super().__new__(cls)
        instance.name = NotInitialized
        return instance
    
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def __getattr__(cls, key: str) -> 'SharedVar':
        return cls.__new__(cls, name=key)

    @staticmethod
    def is_not_initialized(value: Any) -> bool:
        return value is NotInitialized

    def validate(args: Any) -> tuple['SharedVar']:
        if not isinstance(args, tuple):
            raise SharedOnlyAcceptsArguments(args)
        
        args_types = tuple(type(arg) for arg in args)
        for _type in args_types:
            if not issubclass(_type, SharedVar):
                raise SharedAcceptedInvalidArguments(args_types)

        return args



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
                
               *args: Optional[tuple[Any | SharedVar]], 

               ) ->  Callable[..., 
                              Callable[..., 
                                       SharedDefinitionHolder[tuple[SharedVar]]]]:
        
        _vars = None

        def wrapper(func) ->  Callable[..., 
                                       SharedDefinitionHolder[SharedVar]]:

            def _wrapper(*args, **kwargs) -> SharedDefinitionHolder[tuple[SharedVar]]:

                if _vars:
                    return (func, _vars, )
                
                return (func, )


            _shared_reg, _conn_reg = attach_state(func.__globals__, _wrapper.__globals__, mode='shared')
            
            if _conn_reg is None:
                return wrapper
            
            assert hex(id(_wrapper)) not in _shared_reg
            assert hex(id(_wrapper)) not in _conn_reg

            _shared_reg[hex(id(_wrapper))] = _wrapper
            _conn_reg[hex(id(_wrapper))] = hex(id(func))
            
            return _wrapper

        if callable(func):
            if not args:
                return wrapper(func)

            _vars = SharedVar.validate(*args)

        return wrapper


NotInitialized = SharedVar.is_not_initialized
var = SharedVar