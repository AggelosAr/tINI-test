import inspect
import secrets
import textwrap
from collections import deque
from functools import partial
from typing import Any, Callable, Optional, Union, no_type_check

from tini_test._internals._registry import attach_state
from tini_test._internals.consts import _R_M_REG, _R_T_REG, SALT
from tini_test.enums import MockType, Plugs
from tini_test.misc.annotations import (CellName, GlobalRegistry,
                                        IsolateWrappedObject, MaybeRealTest,
                                        MaybeTestFunctionName,
                                        MockDefinitionWrappedHolder,
                                        MockedCBuiltin, MockedClass,
                                        MockedClassInit, MockedFunction,
                                        MockedItem, MockedRawItem,
                                        MockWrappedObject, ProxyItem, RealTest,
                                        SharedDefinitionHolder,
                                        SharedWrappedObject,
                                        SimpleGlobalRegistry, TestFunctionName,
                                        TestWrappedHolder, TestWrappedObject)
from tini_test.misc.exceptions import (DuplicateMockRegisteredOnTest,
                                       MockCallDefinitionError,
                                       MockClassDefinitionError,
                                       MockDefinitionError,
                                       MockMissingFunctionOrClass)
from tini_test.shared import MetaSharedVar, SharedVar, direct_access

_container_types = (list, dict, set)

_meta = MetaSharedVar.get_meta_var()


class MockNone:
    __slots__ = ()


class CreateMock:

    def __init__(self, _type: MockType, mock: MockedItem, view_name: str) -> None:
        self._type = _type
        self.mock = mock
        # Used in combination with the anchor to provide better 
        # identification of the mock in the global namespace
        self._view_name = view_name


        self._proxy_pool: set[str] = set()

        if self._isbuiltin:
            self._mock_backup_store = mock
        else:
            self._mock_backup_store = lambda: None
            self._mock_backup_store.__code__ = self.mock.__code__

        # Used to keep track of the anchor name for this mock in the global namespace
        # Changes after each mock is registered in the global namespace
        # Gets erased when the mock is unregistered from the global namespace
        # Follows the format '_proxy_<mock_name>_<unique_identifier:SALT>'
        self._anchor: str = ''

        # This is the closer we can get to the globals of the test.
        # Should't be a problem since at this point we don't need the 
        # real tests globals but `some` globals.
        # * This happens since we introduced mocking as context manager.
        self._lambda_context: RealTest | MaybeRealTest = lambda: None

    @property
    def _isbuiltin(self) -> bool:
        return self._type == MockType.BUILTIN
    
    @property
    def test(self) -> RealTest | MaybeRealTest:
        return self._lambda_context
    
    @test.setter
    def test(self, value: RealTest | MaybeRealTest) -> None:
        self._lambda_context = value

    @property
    def __globals__(self) -> SimpleGlobalRegistry | GlobalRegistry:
        return self._lambda_context.__globals__
    
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
        self.mock.__code__ = compile(textwrap.dedent(source), '<string>', 'exec').co_consts[0]

    def _restore(self) -> None:
        match self._isbuiltin:

            case True:
                self.__globals__[self.mock.__name__] = self._mock_backup_store
            
            case False:
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
            self.__globals__[self.mock.__name__] = replacement
            return
        
        _, _view_name = self._proxy_generator(use_anchor=True)
        
        anchor, self._anchor = self._proxy_generator(use_anchor=True)

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
            self.__globals__[self.mock.__name__] = replacement
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

        self._test: RealTest | MaybeRealTest = lambda: None

    @property
    def test(self) -> RealTest | MaybeRealTest:
        return self._test

    @test.setter
    def test(self, value: RealTest | MaybeRealTest) -> None:
        self._test = value
        self.body.test = value

    @property
    def test_name(self) -> TestFunctionName | MaybeTestFunctionName:
        return self.test.__name__

    @property
    def __globals__(self) -> SimpleGlobalRegistry | GlobalRegistry:
        return self.test.__globals__

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

    # TODO move these @wrap_utils? and refactor...
    ############################################################################################################
    ############################################################################################################
    @classmethod
    @no_type_check
    def _get_previous_mocks(cls, mock: 'MockDefinition') -> list['MockDefinition']:
        # Find all mocks that have a similar signature in the current namespace
        all_test_mocks = mock.__globals__.get(_R_M_REG, {}).get(mock.test_name, [])
        return list(filter(lambda m: m.body.mock == mock.body.mock, all_test_mocks)) # <

    @classmethod
    @no_type_check
    def register(self, mock: 'MockDefinition') -> None:
        mock.__globals__.setdefault(_R_M_REG, {}).setdefault(mock.test_name, []).append(mock)

    @classmethod
    @no_type_check
    def unregister(cls, mock: 'MockDefinition') -> None:
        mocks = mock.__globals__.get(_R_M_REG).get(mock.test_name)
        new_mocks = list(filter(lambda m: hex(id(m)) != hex(id(mock)), mocks))
        mock.__globals__[_R_M_REG][mock.test_name] = new_mocks

    @classmethod
    @no_type_check
    def get_real_test(cls, 
                      _from: dict[str, Any], 
                      test: RealTest | MaybeRealTest,
                      test_name: TestFunctionName | MaybeTestFunctionName) -> RealTest | MaybeRealTest:
        return _from.get(_R_T_REG, {}).setdefault(test_name, test)
    ############################################################################################################
    ############################################################################################################

    @classmethod
    def add_scope(cls, 
                  mocks: Union['MockDefinition', list['MockDefinition']],
                  test: RealTest | MaybeRealTest) -> None:
        if not isinstance(mocks, list):
            mocks = [mocks]

        for mock in mocks:
            mock.test = test

    def patch(self) -> None:
        self.body._patch()

    def restore(self) -> None:
        self.body._restore()


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
