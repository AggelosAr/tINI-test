import traceback
from contextlib import contextmanager
from traceback import FrameSummary
from typing import Any, Callable, Generator, Literal, Optional

from tini_test._internals._registry import attach_state
from tini_test._internals.consts import SHARED_ID
from tini_test.misc.annotations import (CellName, CellValue, LocalSharedScope,
                                        MockDefinitionWrappedHolder,
                                        MockWrappedObject, RealTest,
                                        SharedDefinitionHolder, SharedMetaId,
                                        SharedWrappedObject, TestCallable,
                                        TestFunctionName, TestWrappedHolder,
                                        TestWrappedObject)
from tini_test.misc.exceptions import (CouldNotFindMetaSharedVar,
                                       GlobalSharedVarsAreNotSupported,
                                       SharedAcceptedInvalidArguments,
                                       SharedOnlyAcceptsArguments,
                                       SharedVarDoesNotExistInThisContext)


class _NotInitialized:
    __slots__ = ()
    
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
    
    def __init__(self, _var: CellName) -> None:
        self._trace = traceback.extract_stack()

        self._stored_key = _var
        self._scope = None

        setattr(self, _var, Cell())

    def __key__(self) -> CellName:
        return object.__getattribute__(self, '_stored_key')

    def __getattribute__(self, 
                         attr: Literal['_trace', 
                                       '_stored_key', 
                                       '_scope', 
                                       '__key__'] | CellName
                         ) -> (list[FrameSummary] 
                               | CellName 
                               | Optional[TestFunctionName] 
                               | CellName
                               | Cell):
        match attr:

            case '_trace':
                return object.__getattribute__(self, '_trace')

            case '_stored_key':
                return object.__getattribute__(self, '_stored_key')
                        
            case '_scope':
                return object.__getattribute__(self, '_scope')

            case '__key__':
                return object.__getattribute__(self, '_stored_key')

            case _:
                stored_key = object.__getattribute__(self, '_stored_key')
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
                raise SharedAcceptedInvalidArguments
            
        return args

    @classmethod
    def add_scope(cls, shared_var: 'SharedVar', scope: TestFunctionName) -> None:
        shared_var._scope = scope


class Shared:

    def __new__(cls, *args: tuple[Any], **kwargs: Any):

        if kwargs:
            raise SharedOnlyAcceptsArguments

        return _XShared.shared(*args)


class _XShared:

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

        # TODO None edge case?
        if func is not None:
            SharedVar.validate(_vars := (func, *args))

        return wrapper


class MetaSharedVar:
    '''
    Dynamic namespaces for shared variables.
    '''
    def __init__(self, 
                 test_name: Optional[TestFunctionName] ='', 
                 _local_context: Optional[LocalSharedScope[SharedVar]] = None) -> None:
        self._test_name = test_name
        self._local_context = _local_context

        self._generating = True
        self._maybe_globals: list[SharedVar] = []

    def __getattr__(self, key: CellName) -> SharedVar | CellValue:
        if self._generating:
            _new = SharedVar(key)
            self._maybe_globals.append(_new)
            return _new
        
        with self.with_lock(key) as shard:
            return shard.key.value

    def __setattr__(self, key: CellName, value: Any) -> None:
        if key in ('_test_name', '_local_context', '_generating', '_maybe_globals'):
            object.__setattr__(self, key, value)
            return

        with self.with_lock(key) as shard:
            shard.key.value = value

    @staticmethod
    def extract_meta_id() -> SharedMetaId:
        return SHARED_ID
    
    @staticmethod
    def extract_meta(_from: TestCallable) -> 'MetaSharedVar':
        meta = _from.__globals__.get(MetaSharedVar.extract_meta_id())
        if meta is None or not isinstance(meta, MetaSharedVar):
            raise CouldNotFindMetaSharedVar(test_name=_from.__name__)
        return meta

    @staticmethod
    def get_context_from_shards(shards: list[SharedVar]) -> LocalSharedScope[SharedVar]:
        return {var.__key__: var for var in shards}
    
    @contextmanager
    def with_lock(self, key: CellName) -> Generator[SharedVar, None, None]:
        try:
            shard = self.access_shard(key)
            
            if shard._scope != self._test_name:
                raise SharedVarDoesNotExistInThisContext(key, self._test_name) # ! 
            
            yield shard

        finally:
            ...

    def raise_for_globals(self) -> None:
        for shard in self._maybe_globals:
            if shard._scope is None:
                _args = (shard.__key__, shard._trace)
                raise GlobalSharedVarsAreNotSupported(*_args)
    
    def reset(self) -> None:
        self._generating = True
        self._maybe_globals = []

    def toggle(self) -> None:
        self._generating = False

    def update_local_context(self, 
                             test_name: TestFunctionName, 
                             context: LocalSharedScope[SharedVar]) -> None:
        self._test_name = test_name
        self._local_context = context

    def test_reset(self) -> None:
        self._test_name = ''
        self._local_context = None

    def access_shard(self, key: CellName) -> SharedVar:

        match self._local_context:
        
            case None:

                raise SharedVarDoesNotExistInThisContext(key, self._test_name)
            
            case _:
                match key in self._local_context:
                
                    case True:
                        shard = self._local_context.get(key)

                        match shard:
                            
                            case None:
                                raise SharedVarDoesNotExistInThisContext(key, self._test_name)
                            case _:
                                return shard
                    
                    case False:
                        raise SharedVarDoesNotExistInThisContext(key, self._test_name)
    


NotInitialized = _NotInitialized
var = MetaSharedVar()