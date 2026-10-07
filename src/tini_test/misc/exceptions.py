from types import FunctionType
from typing import Optional

from tini_test.misc.annotations import CellName, TestFunctionName


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

    def __init__(self, mock_name: str, test_name: TestFunctionName) -> None:
        reason = 'Duplicate mock function < %s > registered on test < %s >' % (mock_name, test_name)
        super().__init__(reason)


class TestDecoratorUsedMoreThanOnce(Exception):

    def __init__(self, test: Optional[FunctionType] = None) -> None:
        if not test:
            test_name = '<unknown>'
        else:
            test_name = test.__name__
        reason = 'Test decorator used more than once on test < %s >' % (test_name, )
        super().__init__(reason)


class MockWasUsedOnWithoutTestDecorator(Exception):

    def __init__(self, test: Optional[FunctionType] = None) -> None:
        if not test:
            test_name = '<unknown>'
        else:
            test_name = test.__name__
        reason = 'Missing test decorator for function decorated with mock function < %s >' % (test_name, )
        super().__init__(reason)


class SharedOnlyAcceptsArguments(Exception):

    def __init__(self) -> None:
        super().__init__('Shared only accepts positional arguments.')


class SharedAcceptedInvalidArguments(Exception):

    def __init__(self) -> None:
        super().__init__('Shared accepts only <var> variables.')


class SharedVarDoesNotExistInThisContext(Exception):

    def __init__(self, var_name: str, test_name: Optional[TestFunctionName] = '') -> None:
        base_msg = 'Shared variable < %s > does not exist in this context.' % (var_name, )
        extra_msg = 'For test < %s >' % (test_name, )
        if test_name:
            msg = '%s %s' % (base_msg, extra_msg, )
        else:
            msg = base_msg
        super().__init__(msg)


class SharedVarAlreadyDefined(Exception):

    def __init__(self, var_name: CellName, test_name: TestFunctionName) -> None:
        msg = 'Shared variable < %s > is already defined in this context. For test < %s >' % (var_name, test_name, )
        super().__init__(msg)
