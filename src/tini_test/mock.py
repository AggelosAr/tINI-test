import inspect
import os
import secrets
import textwrap
import types
from collections import deque
from functools import partial
from types import FrameType
from typing import Any, Callable, Optional, Self, Union, cast

from tini_test._internals._registry import attach_state
from tini_test._internals.consts import _R_M_REG, _R_T_REG, _SETNINEL, SALT
from tini_test.enums import MockType, Plugs
from tini_test.misc.annotations import (CellName, DirectoryPath,
                                        GlobalRegistry, HexStr,
                                        IsolateWrappedObject, MaybeRealTest,
                                        MockDefinitionWrappedHolder,
                                        MockedCBuiltin, MockedClass,
                                        MockedClassInit, MockedFunction,
                                        MockedItem, MockedRawItem,
                                        MockWrappedObject, ProxyItem, RealTest,
                                        SharedDefinitionHolder,
                                        SharedWrappedObject, TestFunctionName,
                                        TestWrappedHolder, TestWrappedObject)
from tini_test.misc.exceptions import (DuplicateMockRegisteredOnTest,
                                       MockCallDefinitionError,
                                       MockClassDefinitionError,
                                       MockDefinitionError,
                                       MockMissingFunctionOrClass)
from tini_test.shared import MetaSharedVar, SharedVar, direct_access


TRACKING_GLOBALS: set[DirectoryPath] = set()

ARTIFACT_TRACKER: list['BuiltInArtifact'] = [] # | _SETNINEL



_container_types = (list, dict, set)

_meta = MetaSharedVar.get_meta_var()


class MockNone:
    __slots__ = ()


class BuiltInArtifact:

    def __init__(self, mock: Union['MockCall', 'MockReturn'], original: Any, replacement: Any) -> None:
        self._name = mock.mock.__name__
        self.original = original
        self.replacement = replacement

        self.mock_anchor = hex(id(mock))

        self.applied_at: list[dict] = []
        
    @property
    def __name__(self) -> str:
        return self._name

    @classmethod
    def get_original_if_exists(cls, obj: Any) -> Callable:
        # In case of a built-in *ONLY* , since we are replacing direcly
        # the global reference to it. We may receive it again as a patched object.
        for artifact in ARTIFACT_TRACKER:
            if artifact is _SETNINEL:
                continue
            if hex(id(artifact.replacement)) == hex(id(obj)):
                return artifact.original
        return obj

    @classmethod
    def restore(cls) -> None:
        for artifact in ARTIFACT_TRACKER:
            if artifact is _SETNINEL:
                continue
            for files_globals in artifact.applied_at:
                files_globals[artifact.__name__] = artifact.original

        TRACKING_GLOBALS.clear()
        ARTIFACT_TRACKER.clear()

    @staticmethod
    def built_in_replacer(apply_at: DirectoryPath, frame: FrameType, event: str, *args):
        _return = partial(BuiltInArtifact.built_in_replacer, apply_at)

        if event != 'call':
            return _return
        
        filename = os.path.abspath(frame.f_code.co_filename)

        # Minor inconveniences ...
        if not filename.startswith(apply_at) or not filename.endswith('.py') or 'site-packages' in filename:
            return _return

        globals_dict = frame.f_globals

        
        if filename not in TRACKING_GLOBALS:

            TRACKING_GLOBALS.add(filename)

            for _artifact in ARTIFACT_TRACKER:

                if _artifact is _SETNINEL:
                    continue

                globals_dict[_artifact.__name__] = _artifact.replacement
                _artifact.applied_at.append(frame.f_globals)

        return _return


class CreateMock:

    def __init__(self, _type: MockType, mock: MockedItem, view_name: str) -> None:
        self._type = _type
        self.mock = mock
        # Used in combination with the anchor to provide better 
        # identification of the mock in the global namespace
        self._view_name = view_name


        self._proxy_pool: set[str] = set()

        if not self._isbuiltin:
            self._mock_backup_store = lambda: None
            self._mock_backup_store = CreateMock.transfer_closure(self._mock_backup_store, self.mock)
            self._mock_backup_store.__code__ = self.mock.__code__

        # Used to keep track of the anchor name for this mock in the global namespace
        # Changes after each mock is registered in the global namespace
        # Gets erased when the mock is unregistered from the global namespace
        # Follows the format '_proxy_<mock_name>_<unique_identifier:SALT>'
        self._anchor: str = ''

        # Test is registered later, hence the <MaybeRealTest>
        # This refers to the context of the test that this mock is associated with.
        # The test doesn't exit until we unwrap the dependency chain,
        # or find it from the globals in the case of the context manager.
        self._lambda_context: RealTest | MaybeRealTest = lambda: None

    @property
    def test(self) -> RealTest:
        return self._lambda_context

    @test.setter
    def test(self, value: RealTest) -> None:
        self._lambda_context = value

    @property
    def _isbuiltin(self) -> bool:
        return self._type == MockType.BUILTIN
    
    @property
    def test_name(self) -> TestFunctionName:
        return self.test.__name__

    @property
    def __globals__(self) -> GlobalRegistry['MockDefinition', SharedVar]:
        return cast(GlobalRegistry['MockDefinition', SharedVar], self._lambda_context.__globals__)

    @staticmethod
    def transfer_closure(target: Callable, source: Callable | types.CodeType) -> Callable:
        cells = source.__closure__ or ()
        _freevars = source.__code__.co_freevars

        # if targer is alredy code object, we just replace the freevars
        if isinstance(target, types.CodeType):
            target = target.replace(co_freevars=_freevars)

            return types.FunctionType(
                target,
                {},
                target.co_name,
                None,
                cells or None,
            )
        else:
            code = target.__code__.replace(co_freevars=_freevars)

            return types.FunctionType(
                code,
                target.__globals__,
                target.__name__,
                target.__defaults__,
                cells or None,
            )
    
    @staticmethod
    def get_var(from_var: bool, _var: SharedVar) -> Any:
        with direct_access(_meta) as meta:
            return meta.__getattr__(_var.__key__) if from_var else _var

    @staticmethod
    def iter_vars(item: Any, 
                  found: dict[CellName, list[SharedVar]],
                  replacer: Callable[[SharedVar], Any]) -> Any:
        # XXX 
        # this should cover all cases????????
        #   This fails in some cases? Like user has registered a class as iter? etc. etc. 
        if isinstance(item, list):
            new_list = []
            for idx, el in enumerate(item):
                item[idx] = CreateMock.iter_vars(el, found, replacer)
                new_list.append(item[idx])
            return new_list

        elif isinstance(item, dict):
            new_dict = {}
            for key, value in item.items():
                new_dict[key] = CreateMock.iter_vars(value, found, replacer)
            return new_dict

        elif isinstance(item, set):
            # SharedVar -> not hashable and not iterable...
            return item
        
        else:
            if isinstance(item, SharedVar):
                found.setdefault(item.__key__, []).append(item)
                return replacer(item)
            
            elif isinstance(item, tuple):
                new_tuple = []

                for el in item:
                    if isinstance(el, SharedVar):
                        found.setdefault(el.__key__, []).append(el)
                        new_tuple.append(replacer(el))
                    elif isinstance(el, _container_types):
                        new_tuple.append(CreateMock.iter_vars(el, found, replacer))
                    else:
                        new_tuple.append(el)

                return tuple(new_tuple)
            else:
                return item

    @staticmethod
    def find_shared(item: Any) -> dict[CellName, list[SharedVar]]:
        found: dict[CellName, list[SharedVar]] = {}
        replacer = partial(CreateMock.get_var, False)
        _ = CreateMock.iter_vars(item, found, replacer)
        return found
    
    @staticmethod
    def replace_shared(item: Any) -> Any:
        replacer = partial(CreateMock.get_var, True)
        return CreateMock.iter_vars(item, found={}, replacer=replacer)

    def get_proxy_name(self, use_anchor: bool) -> str:
        name = self._view_name if use_anchor else ''
        return '_proxy_%s_%s' % (name, secrets.token_hex(SALT), )
    
    def _proxy_generator(self, use_anchor: Optional[bool] = None) -> ProxyItem:
        
        def _proxy(*args, **kwargs): ...

        _proxy.__name__ = self.get_proxy_name(use_anchor if use_anchor is not None else False)

        return ProxyItem(_proxy, _proxy.__name__)

    def _compile_mock(self, source: str) -> None:
        new_code = compile(textwrap.dedent(source), '<string>', 'exec').co_consts[0]
        new_code = CreateMock.transfer_closure(new_code, self.mock)
        self.mock.__code__ = new_code.__code__

    def _restore(self) -> None:
        if self._isbuiltin:
            return
        
        self.mock.__code__ = self._mock_backup_store.__code__
        
        deque(map(lambda x: self.mock.__globals__.pop(x, None), self._proxy_pool), maxlen=0)
        self._proxy_pool.clear()
        self._anchor = ''


class MockCall(CreateMock):

    def __init__(self,
                 _type: MockType,
                 mock: MockedCBuiltin | MockedClassInit | MockedFunction,
                 view_name: str,
                 args: tuple, 
                 kwargs: dict) -> None:
        
        self.args = args
        self.kwargs = kwargs
        
        super().__init__(_type, mock, view_name)

    @property
    def _vars(self) -> dict[CellName, list[SharedVar]]:
        res: dict[CellName, list[SharedVar]] = {}

        for k, v in CreateMock.find_shared(self.args).items():
            res.setdefault(k, []).extend(v)

        for k, v in CreateMock.find_shared(self.kwargs).items():
            res.setdefault(k, []).extend(v)

        return res
    
    @staticmethod
    def validate_call(args: Any, kwargs: Any) -> tuple[tuple, dict]:
        MockCall.validate_args(args)
        MockCall.validate_kwargs(kwargs)
        return args, kwargs

    @staticmethod
    def validate_args(args: Any) -> None:
        if not isinstance(args, tuple):
            raise MockCallDefinitionError('Arguments should be of type tuple. Maybe you forgot a comma?')

    @staticmethod
    def validate_kwargs(kwargs: Any) -> None:
        if not isinstance(kwargs, dict):
            raise MockCallDefinitionError('Keyword arguments should be of type dict.')

    def _patch(self) -> None:
        if self._isbuiltin:
            _args = lambda: CreateMock.replace_shared(self.args)
            _kwargs = lambda: CreateMock.replace_shared(self.kwargs)
            replacement = lambda *args, **kwargs: self.mock(*_args(), **_kwargs())

            ARTIFACT_TRACKER.append(BuiltInArtifact(self, self.mock, replacement))
            return
        
        _, _view_name = self._proxy_generator(use_anchor=True)
        
        anchor, self._anchor = self._proxy_generator(use_anchor=True)
        anchor = CreateMock.transfer_closure(anchor, self.mock)
        
        _, _proxy_locals__args_name = self._proxy_generator()
        _, _proxy_locals__kwargs_name = self._proxy_generator()

        self._proxy_pool.add(_view_name)
        self._proxy_pool.add(self._anchor)
        self._proxy_pool.add(_proxy_locals__args_name)
        self._proxy_pool.add(_proxy_locals__kwargs_name)

        anchor.__signature__ = inspect.signature(self.mock)

        anchor.__code__ = self.mock.__code__

        self.mock.__globals__[self._anchor] = anchor

        _args = lambda: CreateMock.replace_shared(self.args)
        self.mock.__globals__[_proxy_locals__args_name] = _args

        _kwargs = lambda: CreateMock.replace_shared(self.kwargs)
        self.mock.__globals__[_proxy_locals__kwargs_name] = _kwargs

        anchor.__globals__.update(self.mock.__globals__)
        
        new_spec = (
            'def %s(*args, **kwargs):                                         \n'   \
            '    _args, kwargs = globals()["%s"](), globals()["%s"]()         \n'   \
            '    bound = globals()["%s"].__signature__.bind(*_args, **kwargs) \n'   \
            '    bound.apply_defaults()                                       \n'   \
            '    return %s(*bound.args, **bound.kwargs)                       \n'   \
            % 
                (
                    _view_name,
                    _proxy_locals__args_name, _proxy_locals__kwargs_name,
                    self._anchor,
                    self._anchor, 
                )
            )
        self._compile_mock(new_spec)


class MockReturn(CreateMock):

    def __init__(self,
                 _type: MockType,
                 mock: MockedCBuiltin | MockedClassInit | MockedFunction,
                 view_name: str,
                 return_value: Any) -> None:
        
        self.return_value = return_value

        super().__init__(_type, mock, view_name)

    @property
    def _vars(self) -> dict[CellName, list[SharedVar]]:
        return CreateMock.find_shared(self.return_value)
    
    def _patch(self) -> None:
        if self._isbuiltin:
            replacement = lambda *args, **kwargs: CreateMock.replace_shared(self.return_value)
            
            ARTIFACT_TRACKER.append(BuiltInArtifact(self, self.mock, replacement))
            return 
        
        _, _view_name = self._proxy_generator(use_anchor=True)
        _, self._anchor = self._proxy_generator(use_anchor=True)
        
        self._proxy_pool.add(_view_name)
        self._proxy_pool.add(self._anchor)

        _ = lambda: CreateMock.replace_shared(self.return_value)
        self.mock.__globals__[self._anchor] = _

        new_spec = ('def %s(*args, **kwargs): return globals()["%s"]()'
                    % 
                        (
                            _view_name, self._anchor, 
                        )
                    )
        self._compile_mock(new_spec)

    
class MockDefinition:
    
    def __init__(self, body: MockCall | MockReturn) -> None:
        self.body = body

    @property
    def _isbuiltin(self) -> bool:
        return self.body._isbuiltin
    
    @property
    def test(self) -> RealTest:
        return self.body.test

    @test.setter
    def test(self, value: RealTest) -> None:
        self.body.test = value

    @property
    def test_name(self) -> TestFunctionName:
        return self.test.__name__

    @property
    def __globals__(self) -> GlobalRegistry['MockDefinition', SharedVar]:
        return self.body.__globals__

    @property
    def _anchor(self) -> str:
        return self.body._anchor

    @property
    def _vars(self) -> dict[CellName, list[SharedVar]]:
        return self.body._vars
    
    @staticmethod
    def arg_exists(arg: Any) -> bool:
        return type(arg) is not type or not issubclass(arg, MockNone)

    @staticmethod
    def align_mock(mock_type: MockType, mock: MockedRawItem) -> tuple[MockedItem, str]:
        match mock_type:

            case MockType.BUILTIN:
                return mock, mock.__name__
            
            case MockType.CLASS:
                # TODO overrides __new__ ?
                return mock.__init__, '%s_%s' % (mock.__name__, mock.__init__.__name__)
            
            case MockType.FUNCTION:
                return mock, mock.__name__
            
            case _:
                # classmethods and staticmethods are not supported by this Python < 3.12 >.
                raise MockDefinitionError
            
    @staticmethod
    def validate_mock(mock: Any) -> tuple[MockType, MockedItem, str]:
        _mock_exists = MockDefinition.arg_exists(mock)

        if not _mock_exists:
            raise MockMissingFunctionOrClass

        _type, _mock = MockType.get_type(mock)
        if _type and _mock:

            __mock, view_name = MockDefinition.align_mock(_type, _mock)
            return _type, __mock, view_name
        
        raise MockMissingFunctionOrClass

    @staticmethod
    def validate_definition(mock: Any,
                            returns: Any, 
                            args: Any, 
                            kwargs: Any) -> MockCall | MockReturn:
        mock_type, _mock, view_name = MockDefinition.validate_mock(mock)

        _returns_exist = MockDefinition.arg_exists(returns)
        _args_exist = MockDefinition.arg_exists(args)
        _kwargs_exist = MockDefinition.arg_exists(kwargs)

        if _args_exist or _kwargs_exist:

            if _returns_exist:
                raise MockDefinitionError
        
            _args, _kwargs = MockCall.validate_call(() if not _args_exist else args, 
                                                    {} if not _kwargs_exist else kwargs)

            if mock_type == MockType.CLASS:
                _args = (mock, *_args)

            return MockCall(mock_type, _mock, view_name, _args, _kwargs)
        
        if _returns_exist:
    
            if mock_type == MockType.CLASS:
                # TODO implement class ?
                raise MockClassDefinitionError

            # Ignore returns since we can't validate it. It can be an arbitrary value.
            return MockReturn(mock_type, _mock, view_name, returns)

        raise MockDefinitionError
        
    @classmethod
    def raise_for_duplicate_mocks(cls, mocks: list['MockDefinition'], test_name: TestFunctionName) -> None:
        '''
        Raise an error if there are duplicate mocks registered for the same test.
        In case of mocking as context manager, such checks are not done.
        '''
        unique_mocks = set()
        for mock in mocks:
            mocked_function_name = mock.body._view_name

            if mocked_function_name in unique_mocks:
                raise DuplicateMockRegisteredOnTest(mock_name=mocked_function_name, test_name=test_name)
            
            unique_mocks.add(mocked_function_name)

    @classmethod
    def add_scope(cls, 
                  mocks: Union['MockDefinition', list['MockDefinition']],
                  test: RealTest | MaybeRealTest) -> None:
        if not isinstance(mocks, list):
            mocks = [mocks]

        for mock in mocks:
            mock.test = test

    ####################################
    # Mocking utils for context manager
    ####################################
    @classmethod
    def _cx_get_globals(cls, frame: FrameType) -> GlobalRegistry['MockDefinition', SharedVar]:
        _reg = frame.f_globals
        if _R_M_REG not in _reg:
            raise RuntimeError('Global registry for mocks not found') # TODO Exception
        return cast(GlobalRegistry['MockDefinition', SharedVar], _reg)
    
    @classmethod
    def _cx_get_real_test(cls, frame: FrameType | None) -> RealTest:
        if frame is None:
            raise RuntimeError('Frame is None') # TODO Exception

        real_test = cls._cx_get_globals(frame).get(_R_T_REG).get(frame.f_code.co_name)

        if real_test is None:
            raise RuntimeError('Real test not found') # TODO Exception
        
        return real_test
    
    def _cx_cmp_mock_body(_cx_mock: Self, other: 'MockDefinition') -> bool:
        return hex(id(_cx_mock.body.mock)) == hex(id(other.body.mock))

    def _cx_cmp_mock(_cx_mock: Self, other: 'MockDefinition') -> bool:
        return hex(id(_cx_mock)) == hex(id(other))
    
    def _cx_get_previous_mocks(_cx_mock: Self) -> list['MockDefinition']:
        # Find all mocks that have a similar signature in the current namespace
        relevant_mocks = _cx_mock.__globals__[_R_M_REG][_cx_mock.test_name]
        return list(filter(lambda m: _cx_mock._cx_cmp_mock_body(m), relevant_mocks))

    def _cx_register(_cx_mock: Self) -> None:
        _cx_mock.__globals__[_R_M_REG][_cx_mock.test_name].append(_cx_mock)

    def _cx_unregister(_cx_mock: Self) -> None:
        mocks = _cx_mock.__globals__[_R_M_REG][_cx_mock.test_name]
        new_mocks = list(filter(lambda m: not _cx_mock._cx_cmp_mock(m), mocks))
        _cx_mock.__globals__[_R_M_REG][_cx_mock.test_name] = new_mocks
    ####################################

    def patch(self) -> None:
        artifact = self.body._patch()    

    def restore(self) -> None:
        self.body._restore()

    @classmethod
    def patch_all(cls, mocks: list['MockDefinition']) -> None:
        deque(map(lambda mock: mock.patch(), mocks), maxlen=0)
        
    @classmethod
    def restore_all(cls, mocks: list['MockDefinition']) -> None:
        deque(map(lambda mock: mock.restore(), mocks), maxlen=0)
        BuiltInArtifact.restore()


class Mock:
    '''
    A class providing utilities for mocking functions and classes within tests.

    It supports both synchronous and asynchronous test modes, ensuring that
    mocked objects do not interfere with the original implementations during
    `async` mode when using the `mock` method. 
    
    The `mocking` context manager does not
    provide such guarantees and should be used with caution.
    '''
    @staticmethod
    def mock(*args, **kwargs):
        '''
        The object to be mocked can be passed positionally or with the `mock` keyword.

        Args and Kwargs for the mock definition,
        regardless of how they are passed, are accepted as is.
        And are not validated against the function signature.

        * During `async` mode, it is guaranteed that the mocked object will
        not interfere with the original.
        '''
        return _XMock.mock(*args, **kwargs)


class _XMock:
    
    @staticmethod
    def mock(func: None
                   | RealTest
                   | MockedFunction
                   | MockedClass

                   | TestWrappedObject
                   | MockWrappedObject
                   | SharedWrappedObject

                   | IsolateWrappedObject
                   
                   | TestWrappedHolder
                   | MockDefinitionWrappedHolder
                   | SharedDefinitionHolder = None,
             /,
             mock    : Optional[Any] = MockNone,
             *,
             returns : Optional[Any] = MockNone,
             args    : Optional[Any] = MockNone,
             kwargs  : Optional[Any] = MockNone

             ) ->  Callable[..., 
                            Callable[..., 
                                     MockDefinitionWrappedHolder[MockDefinition]]]:
        
        is_empty = (
            returns    == MockNone
            and args   == MockNone
            and kwargs == MockNone
        )
        mock_body = None

        def wrapper(func) -> Callable:
        
            def _wrapper(*args, **kwargs) -> MockDefinitionWrappedHolder[MockDefinition]:
                
                if mock_body:
                    return (func, MockDefinition(mock_body), )

                return (func, )
            
            _mock_reg, _conn_reg = attach_state(func.__globals__, _wrapper.__globals__, mode=Plugs.MOCK)

            if _mock_reg is None or _conn_reg is None:
                return wrapper
            
            assert hex(id(_wrapper)) not in _mock_reg
            assert hex(id(_wrapper)) not in _conn_reg

            _mock_reg[hex(id(_wrapper))] = _wrapper
            _conn_reg[hex(id(_wrapper))] = hex(id(func))

            return _wrapper


        if callable(func):

            if is_empty:
                return wrapper(func)
            else:
                mock = func
                mock_body = MockDefinition.validate_definition(mock, returns, args, kwargs)
        elif not is_empty:
            mock_body = MockDefinition.validate_definition(mock, returns, args, kwargs)
        
        return wrapper
