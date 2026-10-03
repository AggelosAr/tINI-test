import inspect
import secrets
import textwrap
from collections import deque
from typing import Any, Callable, Optional

from tini_test._internals._registry import attach_state
from tini_test.enums import MockMode
from tini_test.misc.annotations import (MockDefinitionWrapperHolder,
                                        MockedFunction, MockWrappedObject,
                                        ProxyItem, TestWrappedObject)
from tini_test.misc.exceptions import (MockCallDefinitionError,
                                       MockDefinitionError,
                                       MockMissingFunctionError)


class MockNone:
    pass


class MockCall:

    mode = MockMode.PATCH_CALL

    def __init__(self, args: Optional[tuple] = None, kwargs: Optional[dict] = None) -> None:
        self.args = args or ()
        self.kwargs = kwargs or {}

    def __str__(self) -> str:
        return 'MockCall(args=%s, kwargs=%s)' % (self.args, self.kwargs, )
    
    @staticmethod
    def validate_call(args: Any, kwargs: Any) -> None:
        MockCall.validate_args(args)
        MockCall.validate_kwargs(kwargs)

    @staticmethod
    def validate_args(args: Any) -> None:
        if not isinstance(args, tuple):
            raise MockCallDefinitionError('Arguments should be of type tuple.')

    @staticmethod
    def validate_kwargs(kwargs: Any) -> None:
        if not isinstance(kwargs, dict):
            raise MockCallDefinitionError('Keyword arguments should be of type dict.')

    def get_default_kwargs(self, spec: inspect.FullArgSpec, sig: inspect.Signature) -> dict:
     
        kwarg_defaults = {
            name: param.default
            for name, param in sig.parameters.items()
            if param.default is not inspect.Parameter.empty
        }

        extra_args = ()
        args = spec.args or []
        defaults = spec.defaults or ()

        if len(self.args) < len(args) and defaults:
            extra_args = defaults[len(args) - len(self.args):]

        extra_kwargs = {}

        for k in kwarg_defaults:
            if k not in self.kwargs:
                extra_kwargs[k] = kwarg_defaults[k]

        return extra_kwargs

    
class MockReturn:

    mode = MockMode.PATCH_RETURN

    def __init__(self, return_value: Any) -> None:
        self.return_value = return_value

    def __str__(self) -> str:
        return 'MockReturn(%s)' % (self.return_value, )


class MockDefinition:
    
    def __init__(self,
                 mock: MockedFunction,
                 *,
                 body: MockCall | MockReturn) -> None:

        self._proxy_pool: set[str] = set()

        self._mock_backup_store = lambda: None
        self._mock_backup_store.__code__ = mock.__code__

        self.mock = mock

        self.body = body
        self.mode = body.mode

    def __str__(self) -> str:
        return 'MockDefinition(%s, %s)' % (self.mock, self.body, )

    @staticmethod
    def arg_exists(arg: Any) -> bool:
        return type(arg) is not type or not issubclass(arg, MockNone)
    
    @staticmethod
    def validate_mock_definition_arguments(returns: Any, 
                                           args: Any, 
                                           kwargs: Any
                                           ) -> MockCall | MockReturn:

        _returns_exist = MockDefinition.arg_exists(returns)
        _args_exist = MockDefinition.arg_exists(args)
        _kwargs_exist = MockDefinition.arg_exists(kwargs)

        if _args_exist or _kwargs_exist:

            if _returns_exist:
                raise MockDefinitionError('Mock should not accept both return value and arguments.')
        
            if not _args_exist:
                args = ()
            if not _kwargs_exist:
                kwargs = {}

            MockCall.validate_call(args, kwargs)

            return MockCall(args=args, kwargs=kwargs)

        
        if _returns_exist:

            if _args_exist or _kwargs_exist:
                raise MockDefinitionError('Mock should not accept both return value and arguments.')

            # Ignore returns since we can't validate it. It can be an arbitrary value.
            return MockReturn(return_value=returns)
        
        raise MockDefinitionError('Mock should accept either a return value or arguments, but not both.')

    def _proxy_generator(self) -> ProxyItem:
    
            def _proxy(*args, **kwargs): ...
    
            _proxy.__name__ = '_proxy_%s' % (secrets.token_hex(10), )
    
            return ProxyItem(_proxy, _proxy.__name__)

    def patch(self) -> None:

        match self.mode:

            case MockMode.PATCH_RETURN:
                self._patch_returns()

            case MockMode.PATCH_CALL:
                self._patch_call()

    def restore(self) -> None:
        self.mock.__code__ = self._mock_backup_store.__code__
        deque(map(lambda x: self.mock.__globals__.pop(x, None), self._proxy_pool), maxlen=0)
        self._proxy_pool.clear()

    def _compile_mock(self, source: str) -> None:
        self.mock.__code__ = compile(textwrap.dedent(source), 
                                     '<string>', 
                                     'exec').co_consts[0]

    def _patch_returns(self) -> None:

        _, _proxy_name = self._proxy_generator()
        _, _proxy_return_name = self._proxy_generator()
        
        self._proxy_pool.add(_proxy_name)
        self._proxy_pool.add(_proxy_return_name)

        self.mock.__globals__[_proxy_return_name] = self.body.return_value

        new_spec = ('def _%s(*args, **kwargs): return globals()["%s"]' 
                    % 
                        (
                            _proxy_name,
                            _proxy_return_name, 
                        )
                    )
        self._compile_mock(new_spec)
    
    def _patch_call(self) -> None:

        _, _proxy_name = self._proxy_generator()
        _proxy_x, _proxy_x_name = self._proxy_generator()
        _, _proxy_locals__args_name = self._proxy_generator()
        _, _proxy_locals__kwargs_name = self._proxy_generator()

        self._proxy_pool.add(_proxy_name)
        self._proxy_pool.add(_proxy_x_name)
        self._proxy_pool.add(_proxy_locals__args_name)
        self._proxy_pool.add(_proxy_locals__kwargs_name)

        _proxy_x.__code__ = self.mock.__code__

        self.mock.__globals__[_proxy_x_name] = _proxy_x
        self.mock.__globals__[_proxy_locals__args_name] = self.body.args

        spec = inspect.getfullargspec(self.mock)
        sig = inspect.signature(self.mock)
        default_kwargs = self.body.get_default_kwargs(spec, sig)

        self.mock.__globals__[_proxy_locals__kwargs_name] = {**self.body.kwargs, **default_kwargs}

        _proxy_x.__globals__.update(self.mock.__globals__)
        
        new_spec = ('def _%s(*args, **kwargs): return %s(*globals()["%s"], **globals()["%s"])' 
                    % 
                        (
                            _proxy_name,
                            _proxy_x_name, 
                            _proxy_locals__args_name,
                            _proxy_locals__kwargs_name,

                        )
                    )
        self._compile_mock(new_spec)


class Mock:
    """
    Args and Kwargs for the mock definition.
    Are accepted as is. And are not validated 
    against the function signature.
    """

    @classmethod
    def mock(cls,
             func: None
                   | Callable
                   | MockWrappedObject 
                   | TestWrappedObject = None, 
             /,
             mock    : Optional[Any] = MockNone,
             returns : Optional[Any] = MockNone,
             args    : Optional[tuple[Any]] = MockNone,
             kwargs  : Optional[dict[Any, Any]] = MockNone):
        
        is_empty = (
            returns == MockNone
            and args == MockNone
            and kwargs == MockNone
        )
        mock_body = None
        _test_func = None


        def wrapper(func) -> Callable[..., 
                                      Callable[..., 
                                               MockDefinitionWrapperHolder[MockDefinition]]]:
        
            # ...

            def _wrapper(*args, **kwargs) -> MockDefinitionWrapperHolder[MockDefinition]:

                _func = (func or _test_func)
                
                if mock_body:
                    
                    return (_func, MockDefinition(mock, body=mock_body), )

                return (_func, )

            if (func is None or not MockDefinition.arg_exists(mock)) and not is_empty:
                raise MockMissingFunctionError()
            
            _mock_reg, _conn_reg = attach_state(func.__globals__, _wrapper.__globals__, mode='mock')

            if _conn_reg is None:
                return wrapper
            
            assert hex(id(_wrapper)) not in _mock_reg
            assert hex(id(_wrapper)) not in _conn_reg

            _mock_reg[hex(id(_wrapper))] = _wrapper
            _conn_reg[hex(id(_wrapper))] = hex(id(func))

            return _wrapper


        if callable(func):

            _test_func = func
            if is_empty:
                return wrapper(func)
            else:
                mock = func
                mock_body = MockDefinition.validate_mock_definition_arguments(returns, args, kwargs)
        
        return wrapper
