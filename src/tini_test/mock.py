import textwrap
from typing import Any, Callable, Optional

from tini_test._internals._registry import _CONN, _MOCK_REGISTRY
from tini_test.enums import MockMode
from tini_test.misc.annotations import (MockedFunction, MockWrappedObject,
                                        TestWrappedObject)
from tini_test.misc.exceptions import (MockCallDefinitionError,
                                       MockDefinitionError,
                                       MockMissingFunctionError)


# TODO Not correct?
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

        self._store = lambda: None
        self._store.__code__ = mock.__code__

        # TODO inform the type checker about the type of self.body based on self.mode
        # Is that possible?

        self.body = body
        self.mode = body.mode

        self.mock = mock

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
    
    def patch(self) -> None:

        match self.mode:

            case MockMode.PATCH_RETURN:
                self._patch_returns()

            case MockMode.PATCH_CALL:
                self._patch_call()

    # HOW DO WE TEST ON ASYNC?
    def restore(self) -> None:
        self.mock.__code__ = self._store.__code__
       
    def _patch_returns(self) -> None:

        x = textwrap.dedent(
                    (
                        'def _(*args, **kwargs): return %s' % (self.body.return_value, )
                    )
                )
        self.mock.__code__ = compile(x, '<string>', 'exec').co_consts[0]

    def _patch_call(self):
        _res = self.mock(*self.body.args, **self.body.kwargs)
        self.body.return_value = _res
        self._patch_returns()



class Mock:
    
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

        def wrapper(func):
        

            def _wrapper(*args, **kwargs):

                if mock_body:
                    return (func or _test_func, MockDefinition(mock, body=mock_body), )

                return (func or _test_func, )

            if (func is None or not MockDefinition.arg_exists(mock)) and not is_empty:
                raise MockMissingFunctionError('Mock function is missing.')

            # TODO here we should add the signature validation.

            assert hex(id(_wrapper)) not in _MOCK_REGISTRY
            assert hex(id(_wrapper)) not in _CONN

            _MOCK_REGISTRY[hex(id(_wrapper))] = _wrapper
            _CONN[hex(id(_wrapper))] = hex(id(func))

            return _wrapper


        if callable(func):

            _test_func = func
            if is_empty:
                return wrapper(func)
            else:
                mock = func
                mock_body = MockDefinition.validate_mock_definition_arguments(returns, args, kwargs)
        
        return wrapper
