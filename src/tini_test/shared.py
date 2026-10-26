import traceback
from contextlib import contextmanager
from traceback import FrameSummary
from typing import Any, Callable, Generator, Literal, Optional

from tini_test._internals._registry import attach_state
from tini_test.enums import Plugs
from tini_test.misc.annotations import (CellName, CellValue,
                                        IsolateWrappedObject, LocalSharedScope,
                                        MockDefinitionWrappedHolder,
                                        MockWrappedObject, RealTest,
                                        SharedDefinitionHolder,
                                        SharedWrappedObject, TestFunctionName,
                                        TestWrappedHolder, TestWrappedObject)
from tini_test.misc.exceptions import (GlobalSharedVarsAreNotSupported,
                                       SharedAcceptedInvalidArguments,
                                       SharedOnlyAcceptsArguments,
                                       SharedVarAlreadyDefined,
                                       SharedVarDoesNotExistInThisContext)


class _NotInitialized:
    __slots__ = ()


class Cell:
    __slots__ = ('value', )

    def __init__(self, value: Optional[Any] = _NotInitialized) -> None:
        self.value = value


class SharedVar:

    def __new__(cls, *args, **kwargs) -> 'SharedVar':
        instance = super().__new__(cls)
        return instance

    def __init__(self, key: CellName) -> None:
        self._trace = traceback.extract_stack()

        self._stored_key = key
        self._scope = None

        self._stored_value = Cell()

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
                stored_value = object.__getattribute__(self, '_stored_value')
                return stored_value
    
    @classmethod
    def validate(cls, args: Any) -> tuple['SharedVar']:
        args_types = tuple(type(arg) for arg in args)

        for _type in args_types:
            if not issubclass(_type, SharedVar):
                raise SharedAcceptedInvalidArguments

        return args

    @classmethod
    def raise_for_duplicate_vars(cls, shared_vars: list['SharedVar'], test_name: TestFunctionName) -> None:
        unique_shared_vars = set()
        
        for shared_var in shared_vars:
            if shared_var.__key__ in unique_shared_vars:
                raise SharedVarAlreadyDefined(var_name=shared_var.__key__, test_name=test_name)
            unique_shared_vars.add(shared_var.__key__)

    @classmethod
    def add_scope(cls, shared_vars: list['SharedVar'], scope: TestFunctionName) -> None:
        for shared_var in shared_vars:
            shared_var._scope = scope


class Shared:
    '''
    The `@Shared` decorator is used to define shared variables that can be accessed
    across the lifecycle of the test.

    It ensures that the shared variables are properly scoped and prevents 
    duplicate definitions within the same test.
    '''
    def __new__(cls, *args: tuple[Any], **kwargs: Any):

        if kwargs:
            raise SharedOnlyAcceptsArguments

        if any(arg is None for arg in args):
            raise SharedAcceptedInvalidArguments

        return _XShared.shared(*args)


class _XShared:

    @classmethod
    def shared(cls,
               func: None
                     | RealTest 

                     | TestWrappedObject
                     | MockWrappedObject
                     | SharedWrappedObject

                     | IsolateWrappedObject
                     
                     | TestWrappedHolder
                     | MockDefinitionWrappedHolder
                     | SharedDefinitionHolder = None,
                
               *args: Optional[tuple[Any | SharedVar]], 

               ) ->  Callable[..., 
                              Callable[..., 
                                       SharedDefinitionHolder[tuple[SharedVar]]]]:
        
        _vars = None

        def wrapper(func) ->  Callable:

            def _wrapper(*args, **kwargs) -> SharedDefinitionHolder[tuple[SharedVar]]:

                return (func, ) if not _vars else (func, _vars, )
            
            _shared_reg, _conn_reg = attach_state(func.__globals__, _wrapper.__globals__, mode=Plugs.SHARED)

            if _shared_reg is None or _conn_reg is None:
                return wrapper
            
            assert hex(id(_wrapper)) not in _shared_reg
            assert hex(id(_wrapper)) not in _conn_reg

            _shared_reg[hex(id(_wrapper))] = _wrapper
            _conn_reg[hex(id(_wrapper))] = hex(id(func))
            
            return _wrapper

        if callable(func) and not args:
            return wrapper(func)
        
        if func is not None:
            _args = (func, *args)
            _vars = SharedVar.validate(_args)

        return wrapper


@contextmanager
def direct_access(obj: 'MetaSharedVar') -> Generator['MetaSharedVar', None, None]:
    object.__setattr__(obj, '_direct_mode', True)
    try:
        yield obj
    finally:
        object.__setattr__(obj, '_direct_mode', False)


class MetaSharedVar:
    '''
    Dynamic namespaces for shared variables.
    '''
    def __init__(self, 
                 test_name: Optional[TestFunctionName] ='', 
                 _local_context: Optional[LocalSharedScope[SharedVar]] = None) -> None:
        object.__setattr__(self, '_generating', True)
        object.__setattr__(self, '_maybe_globals', [])
        object.__setattr__(self, '_test_name', test_name)
        object.__setattr__(self, '_local_context', _local_context)
    
    def __generating(self) -> bool:
        return object.__getattribute__(self, '_generating')
    
    def __maybe_globals(self) -> list[SharedVar]:
        return object.__getattribute__(self, '_maybe_globals')
    
    def __test_name(self) -> TestFunctionName:
        return object.__getattribute__(self, '_test_name')
    
    def __local_context(self) -> LocalSharedScope[SharedVar] | None:
        return object.__getattribute__(self, '_local_context')
    
    def __getattribute__(self, name):
        if object.__getattribute__(self, '_direct_mode'):
            return object.__getattribute__(self, name)
        
        return object.__getattr__(self, name)
        
    def __getattr__(self, key: CellName) -> SharedVar | CellValue:
        with direct_access(self) as _self:
            if _self.__generating():
                _new = SharedVar(key)
                _self.__maybe_globals().append(_new)
                return _new
        
            with _self.with_lock(key) as shard:
                return shard.key.value

    def __setattr__(self, key: CellName, value: Any) -> None:
        with direct_access(self) as _self:
            with _self.with_lock(key) as shard:
                shard.key.value = value

    @classmethod
    def get_meta_var(cls) -> 'MetaSharedVar':
        return var

    @staticmethod
    def get_context_from_shards(shards: list[SharedVar]) -> LocalSharedScope[SharedVar]:
        return {var.__key__: var for var in shards}
    
    @contextmanager
    def with_lock(self, key: CellName) -> Generator[SharedVar, None, None]:
        try:

            shard = self.access_shard(key)
        
            if shard._scope != self.__test_name():
                raise SharedVarDoesNotExistInThisContext(key, self.__test_name())
        
            yield shard

        finally:
            ...
        
    def raise_for_globals(self) -> None:
        for shard in self.__maybe_globals():
            if shard._scope is None:
                _args = (shard.__key__, shard._trace)
                raise GlobalSharedVarsAreNotSupported(*_args)
    
    def reset(self) -> None:
        object.__setattr__(self, '_generating', True)
        object.__setattr__(self, '_maybe_globals', [])

    def block(self) -> None:
        object.__setattr__(self, '_generating', False)

    def update_local_context(self, 
                             test_name: TestFunctionName, 
                             context: LocalSharedScope[SharedVar]) -> None:
        object.__setattr__(self, '_test_name', test_name)
        object.__setattr__(self, '_local_context', context)

    def test_reset(self) -> None:
        object.__setattr__(self, '_test_name', '')
        object.__setattr__(self, '_local_context', None)

    def access_shard(self, key: CellName) -> SharedVar:

        match self.__local_context():
        
            case None:
                raise SharedVarDoesNotExistInThisContext(key, self.__test_name())
            
            case _:
                match key in self.__local_context():
                
                    case True:
                        shard = self.__local_context().get(key)

                        match shard:
                            
                            case None:
                                raise SharedVarDoesNotExistInThisContext(key, self.__test_name())
                            
                            case _:
                                return shard        
                    
                    case False:
                        raise SharedVarDoesNotExistInThisContext(key, self.__test_name())


NotInitialized = _NotInitialized
var = MetaSharedVar()