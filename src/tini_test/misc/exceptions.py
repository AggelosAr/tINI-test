from types import FunctionType

# TODO split these Exceptions into groups...

class NotSupportedVerbosity(Exception):

    def __init__(self, msg: str = ''):
        super().__init__(msg)


class NotSupportedRunMode(Exception):

    def __init__(self, msg: str = '') -> None:
        super().__init__(msg)


class CantFindRelativePathToRoot(Exception):

    def __init__(self) -> None:
        super().__init__("Can't find the requested relative path to root.")


class TestNotFound(Exception):

    def __init__(self, extra_msg: str = '') -> None:
        super().__init__('Test function was not found.\n\t%s' % (extra_msg, ))


class WillRaiseReceivedNotAnException(Exception):

    def __init__(self) -> None:
        super().__init__('Objects passed to WillRaise should be exceptions.')


class ExpectedWasDifferentFromActual(Exception):
    def __init__(self, msg: str = '') -> None:
        super().__init__(msg)
        self.msg = msg
    
    def _get_detail(self) -> str:
        return f'\n{self.msg}\n[EOD]'

  
class ComperatorWasNotProvided(Exception):

    def __init__(self) -> None:
        super().__init__('Unknown type encountered and a comperator was not provided.')


class ComperatorIsNotValid(Exception):

    def __init__(self, reason: str = '') -> None:
        super().__init__(reason)


class ExceptionWasNotRaised(Exception):

    def __init__(self, reason: str = '') -> None:
        super().__init__(reason)


class MockDefinitionError(Exception):

    def __init__(self, reason: str = '') -> None:
        super().__init__(reason)


class MockCallDefinitionError(Exception):

    def __init__(self, reason: str = '') -> None:
        super().__init__(reason)


class MockMissingFunctionError(Exception):

    def __init__(self, reason: str = '') -> None:
        reason = 'Mock function is missing.'
        super().__init__(reason)


class DuplicateMockRegisteredOnTest(Exception):

    def __init__(self, mock_function: str = '', test_name: str = '') -> None:
        reason = 'Duplicate mock function < %s > registered on test < %s >' % (mock_function, test_name)
        super().__init__(reason)


class TestDecoratorUsedMoreThanOnce(Exception):

    def __init__(self, test_name: str = '') -> None:
        reason = 'Test decorator used more than once on test < %s >' % (test_name, )
        super().__init__(reason)


class MockWasUsedOnWithoutTestDecorator(Exception):

    def __init__(self, test_func: FunctionType | None = None) -> None:
        if not test_func:
            test_name = '<unknown>'
        else:
            test_name = test_func.__name__
        reason = 'Missing test decorator for function decorated with mock function < %s >' % (test_name, )
        super().__init__(reason)


class SharedOnlyAcceptsArguments(Exception):

    def __init__(self) -> None:
        super().__init__('Shared only accepts arguments.')


class SharedAcceptedInvalidArguments(Exception):

    def __init__(self, args_types: tuple[type, ...]) -> None:
        super().__init__('Shared accepted not valid argument. Types received: %s' % (args_types, ))


class SharedVarDoesNotExistInThisContext(Exception):

    def __init__(self, var_name: str = '', test_name: str = '') -> None:
        msg = 'Shared variable < %s > does not exist in this context for test < %s >.' % (var_name, test_name, )
        super().__init__(msg)


class SharedVarAlreadyDefined(Exception):

    def __init__(self, var_name: str = '', test_name: str = '') -> None:
        msg = 'Shared variable < %s > is already defined in this context for test < %s >.' % (var_name, test_name, )
        super().__init__(msg)
