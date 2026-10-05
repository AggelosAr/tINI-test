from typing import Any, Callable, Generator, Optional

from tini_test._internals._registry import attach_state
from tini_test.misc.annotations import (MockDefinitionWrappedHolder,
                                        MockWrappedObject, RealTest,
                                        SharedDefinitionHolder,
                                        SharedWrappedObject, TestCallables,
                                        TestWrappedHolder, TestWrappedObject)
from tini_test.misc.exceptions import (SharedAcceptedInvalidArguments,
                                       SharedOnlyAcceptsArguments)

# Fast solution
SHAREDS = {}


class _NotInitialized:
    object

    @staticmethod # TODO
    def is_not_initialized(_var: Any) -> bool:
        return type(_var) is not type or not issubclass(_var, _NotInitialized)


class Cell:
    __slots__ = ('value', )

    def __init__(self, value: Optional[Any] = _NotInitialized) -> None:
        self.value = value


class SharedVar:

    def __new__(cls, *args, **kwargs) -> 'SharedVar':
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, _var: str, _initializing: Optional[bool] = False) -> None:
        self.stored_key = _var
        self._initialized = True
        setattr(self, _var, Cell())

    def __getattr__(self, _: Any) -> Cell:
        raise RuntimeError

    def __getattribute__(self, _: Any) -> _NotInitialized | Any:
        if self._initialized:
            return SHAREDS[hex(id(self))]
        
        stored_key = object.__getattribute__(self, 'stored_key')
        return object.__getattribute__(self, stored_key)
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SharedVar):
            return False
        return self._var.value == other._var.value

    @classmethod
    def validate(cls, args: Any) -> tuple['SharedVar']:
        if not isinstance(args, tuple):
            raise SharedOnlyAcceptsArguments(args)
        
        args_types = tuple(type(arg) for arg in args)
        for _type in args_types:
            if not issubclass(_type, SharedVar):
                raise SharedAcceptedInvalidArguments(args_types)

        for item in args:
            SHAREDS[hex(id(item))] = item

        return args

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

                return (func, ) if not _vars else (func, _vars, )


            _shared_reg, _conn_reg = attach_state(func.__globals__, _wrapper.__globals__, mode='shared')
            
            if _conn_reg is None:
                return wrapper
            
            assert hex(id(_wrapper)) not in _shared_reg
            assert hex(id(_wrapper)) not in _conn_reg

            _shared_reg[hex(id(_wrapper))] = _wrapper
            _conn_reg[hex(id(_wrapper))] = hex(id(func))
            
            return _wrapper

        if callable(func) and not args:
            return wrapper(func)

        if func is not None:
            SharedVar.validate(_vars := (func, *args))

        return wrapper


NotInitialized = SharedVar('value', _initializing=True)

class MetaSharedVar:

    def __getattr__(self, key: str) -> SharedVar:
        return next(MetaSharedVar.creator(key))

    @classmethod
    def creator(cls, key: str) -> Generator[SharedVar, None, None]:
        while True:
            yield SharedVar(key, _initializing=True)

var = MetaSharedVar()