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


# TODO Not correct? @NoneTypes
class MockNone:
    pass


class MockCall:

    mode = MockMode.PATCH_CALL

    # TODO at least one is required. Fix type
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

    def unpack_args(self, extra: tuple) -> str:
        args_str = ', '.join(
            '%s'
            %
                (
                    v,
                )
                for v in (*self.args, *extra)
        )
        return args_str

    def unpack_kwargs(self, extra: dict) -> str:
        kwargs_str = ', '.join(
            '%s=%s'
            %
                (
                    k, v,
                )
                for k, v in {**self.kwargs, **extra}.items()
        )
        return kwargs_str

    def unpack_body(self, spec: inspect.FullArgSpec, sig: inspect.Signature) -> str:
        # XXX This is izi if we pay attention to what we are doing.
        # The user provided args and or kwargs.
        # We only need to see if there are defaults that are missing
        # for each case. 
        # Edge case. *args and **kwargs in the function signature. I think we are covered here. *** TEST TODO

        # **args exists = fullargspec.varargs=<NAME> or None?? do we need it ? i dont think so since we are padding anyway 
        # We may need to padd the ARGS with defaults.
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

        # Then we need to pad kwargs as well with defauls.
        # izi pizi
       
        # **kwargs exists = fullargspec.varkw=<NAME> or None do we need it ? i dont think so since we are padding anyway 
        extra_kwargs = {}

        for k in kwarg_defaults:
            if k not in self.kwargs:
                extra_kwargs[k] = kwarg_defaults[k]

        args_str = self.unpack_args(extra_args)
        kwargs_str = self.unpack_kwargs({**extra_kwargs})

        return ', '.join(filter(None, [args_str, kwargs_str]))


class MockReturn:

    mode = MockMode.PATCH_RETURN

    def __init__(self, return_value: Any) -> None:
        self.return_value = return_value

    def __str__(self) -> str:
        return 'MockReturn(%s)' % (self.return_value, )

    def unpack_body(self, spec: Optional[Any] = None) -> Any:
        return self.return_value


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
        
        self._proxy_pool.add(_proxy_name)

        new_spec = ('def _%s(*args, **kwargs): return %s' 
                    % 
                        (
                            _proxy_name,
                            self.body.unpack_body(), 
                        )
                    )
        self._compile_mock(new_spec)
    
    def _patch_call(self) -> None:

        _proxy_a, _proxy_a_name = self._proxy_generator()
        _, _proxy_b_name = self._proxy_generator()

        self._proxy_pool.add(_proxy_a_name)
        self._proxy_pool.add(_proxy_b_name)

        _proxy_a.__code__ = self.mock.__code__

        self.mock.__globals__[_proxy_a_name] = _proxy_a

        # Also we need to update the _proxy_a globals with mocks globals
        # TODO is this efficient???
        # TODO collisions?
        _proxy_a.__globals__.update(self.mock.__globals__)


        spec = inspect.getfullargspec(self.mock)
        sig = inspect.signature(self.mock)

        new_spec = ('def _%s(*args, **kwargs): return %s(%s)' 
                    % 
                        (
                            _proxy_b_name,
                            _proxy_a_name, 
                            self.body.unpack_body(spec=spec, sig=sig), 
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
             args    : Optional[Any] = MockNone,
             kwargs  : Optional[Any] = MockNone):
        
    
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
