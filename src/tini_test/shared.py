from types import FunctionType
from typing import Any, Callable, Generator, Literal, Optional, assert_never

from tini_test._internals._registry import attach_state
from tini_test.misc.annotations import (CellName, CellValue,
                                        MockDefinitionWrappedHolder,
                                        MockWrappedObject, RealTest,
                                        SharedDefinitionHolder, SharedMetaId,
                                        SharedScope, SharedWrappedObject,
                                        TestWrappedHolder, TestWrappedObject)
from tini_test.misc.exceptions import (SharedAcceptedInvalidArguments,
                                       SharedOnlyAcceptsArguments,
                                       SharedVarDoesNotExistInThisContext)


class _NotInitialized:
    object

    @staticmethod
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
    
    def __init__(self, _var: str) -> None:
        self.stored_key = _var
        setattr(self, _var, Cell())

    def __key__(self) -> str:
        return object.__getattribute__(self, 'stored_key')

    def __getattr__(self, _: Any) -> Cell:
        raise RuntimeError

    def __getattribute__(self, attr: Literal['__key__'] | str) -> CellName | Cell:
        stored_key = object.__getattribute__(self, 'stored_key')
        if attr == '__key__':
            return object.__getattribute__(self, 'stored_key')

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


class MetaSharedVar:

    def __init__(self, _context: Optional[SharedScope[SharedVar]] = None):
        self._context = _context

    def __getattr__(self, key: str) -> SharedVar | CellValue:
        if self._context is None:
            return next(MetaSharedVar.new(key))
        
        return self.access_shard(key).key.value

    def __setattr__(self, key: str, value: Any) -> None:
        if key == '_context':
            object.__setattr__(self, key, value)
            return

        self.access_shard(key).key.value = value

    @staticmethod
    def get_context_from_shards(shards: list[SharedVar]) -> SharedScope[SharedVar]:
        return {var.__key__: var for var in shards}

    @staticmethod
    def extract_meta() -> SharedMetaId:
        return 'var'
    
    @classmethod
    def set_new_meta(cls, 
                     meta_id: SharedMetaId, 
                     apply_at: FunctionType,
                     new_meta: 'MetaSharedVar') -> 'MetaSharedVar':
        apply_at.__globals__[meta_id] = new_meta
        return new_meta

    @classmethod
    def new(cls, key: str) -> Generator[SharedVar, None, None]:
        while True:
            yield SharedVar(key)

    @classmethod
    def with_context(cls, context: SharedScope[SharedVar]) -> 'MetaSharedVar':
        return cls(_context=context)
    
    @classmethod
    def with_access_scope(cls, func: list[FunctionType | None]) -> 'MetaSharedVar':
        raise NotImplementedError
    
    def access_shard(self, key: str) -> SharedVar:
        match self._context:
        
            case None:
                raise assert_never
            
            case _:
                match key in self._context:
                
                    case True:
                        shard = self._context.get(key)

                        match shard:
                            
                            case None:
                                raise SharedVarDoesNotExistInThisContext(key)
                            case _:
                                return shard
                    
                    case False:
                        raise SharedVarDoesNotExistInThisContext(key)
    



NotInitialized = _NotInitialized
var = MetaSharedVar()