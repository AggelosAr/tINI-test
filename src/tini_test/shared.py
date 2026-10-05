from typing import Any, Callable, Generator, Optional

from tini_test._internals._registry import attach_state
from tini_test.misc.annotations import (MockDefinitionWrappedHolder,
                                        MockWrappedObject, RealTest,
                                        SharedDefinitionHolder,
                                        SharedWrappedObject, TestCallables,
                                        TestWrappedHolder, TestWrappedObject)
from tini_test.misc.exceptions import (SharedAcceptedInvalidArguments,
                                       SharedOnlyAcceptsArguments)


class NotInitialized:
    object


class SharedVar:

    def __new__(cls, *args, **kwargs) -> 'SharedVar':
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, key: str) -> None:
        setattr(self, key, NotInitialized)

    @classmethod
    def __getattr__(cls, key: str) -> 'SharedVar':
        return cls.__new__(cls, key=key)

    @classmethod
    def validate(cls, args: Any) -> tuple['SharedVar']:
        if not isinstance(args, tuple):
            raise SharedOnlyAcceptsArguments(args)
        
        args_types = tuple(type(arg) for arg in args)
        for _type in args_types:
            if not issubclass(_type, SharedVar):
                raise SharedAcceptedInvalidArguments(args_types)

        return args

    @staticmethod # TODO fix
    def is_not_initialized(value: Any) -> bool:
        return value is NotInitialized

    @staticmethod
    def enable(scopes: list[TestCallables], _var: list['SharedVar']) -> None:
        scope.update({var.key: var for var in _var})

    @staticmethod
    def get(value: 'SharedVar') -> str:
        return value.key

    @staticmethod
    def update(scope, _var: 'SharedVar') -> None:
        scope[_var.key] = _var



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

class MetaSharedVar:

    def __getattr__(self, key: str) -> SharedVar:
        return next(MetaSharedVar.creator(key))

    @classmethod
    def creator(cls, key: str) -> Generator[SharedVar, None, None]:
        while True:
            yield SharedVar(key)

var = MetaSharedVar()