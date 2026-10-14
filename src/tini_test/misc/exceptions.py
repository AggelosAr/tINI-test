import traceback
from traceback import StackSummary
from typing import Optional

from tini_test._internals.consts import _RESET, capture_flag
from tini_test.misc.annotations import (CellName, RealTest, StackTrace,
                                        TestFunctionName)

RED = '\033[91m'
# XXX APPLY colors to our exceptions for better readability


class NotSupportedVerbosity(Exception):

    def __init__(self, msg: str = ''):
        super().__init__(msg)


class NotSupportedRunMode(Exception):

    def __init__(self, msg: str = '') -> None:
        super().__init__(msg)


class CantFindRelativePathToRoot(Exception):

    def __init__(self) -> None:
        super().__init__("Can't find the requested relative path to root.")


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


class MockMissingFunctionError(Exception):

    def __init__(self) -> None:
        super().__init__('Mock function is missing.')


class MockDefinitionError(Exception):

    def __init__(self) -> None:
        super().__init__('Mock should not accept both return value and arguments.')


class MockCallDefinitionError(Exception):

    def __init__(self, reason: str = '') -> None:
        super().__init__(reason)


class DuplicateMockRegisteredOnTest(Exception):

    def __init__(self, mock_name: str, test_name: TestFunctionName) -> None:
        reason = 'Duplicate mock function < %s > registered on test < %s >' % (mock_name, test_name)
        super().__init__(reason)


class TestDecoratorUsedMoreThanOnce(Exception):

    def __init__(self, test: Optional[RealTest | TestFunctionName] = None) -> None:
        if not test:
            test_name = '<unknown>'
        else:
            if isinstance(test, str):
                test_name = test
            else:
                test_name = test.__name__

        if test_name == '_wrapper':
            test_name = '<unknown>'
            
        reason = 'Test decorator used more than once on test < %s >' % (test_name, )
        super().__init__(reason)


class MockWasUsedOnWithoutTestDecorator(Exception):

    def __init__(self, test: Optional[RealTest] = None) -> None:
        if not test:
            test_name = '<unknown>'
        else:
            test_name = test.__name__

        reason = 'Missing test decorator for function decorated with mock function < %s >' % (test_name, )
        super().__init__(reason)


class SharedWasUsedOnWithoutTestDecorator(Exception):

    def __init__(self, test: Optional[RealTest] = None) -> None:
        if not test:
            test_name = '<unknown>'
        else:
            test_name = test.__name__

        reason = 'Missing test decorator for function decorated with Shared < %s >' % (test_name, )
        super().__init__(reason)


class IsolateWasUsedOnWithoutTestDecorator(Exception):

    def __init__(self, test: Optional[RealTest] = None) -> None:
        if not test:
            test_name = '<unknown>'
        else:
            test_name = test.__name__

        reason = 'Missing test decorator for function decorated with Isolate < %s >' % (test_name, )
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


class TestArgumentsShouldBeCallables(Exception):

    def __init__(self, test_name: Optional[TestFunctionName]='') -> None:
        msg = 'Test received as argument(s) not callable(s)'
        super().__init__(msg)


class GlobalSharedVarsAreNotSupported(Exception):

    def __init__(self, var_name: CellName, stack_trace: Optional[StackSummary] = None) -> None:
        msg = self.format_msg(var_name, stack_trace)
        super().__init__(msg)

    def format_exception(self, stack_trace: StackSummary) -> StackTrace:
        captured_frames = []
        capturing = False
        
        for item in stack_trace:
            if capturing:
                captured_frames.append(item)
            if all(flag in str(item) for flag in capture_flag):
                capturing = True
        
        # TODO 
        # Apply color formatting to the captured frames
        # Apply also back ground black colour 
        lines = traceback.format_list(captured_frames)
    
        longest = 0
        for line in lines:
            longest = max(longest, len(line))

        
        msg = ''.join(lines)
        # Pad the lines with the lentgh of the longest in white space 
        # e.g. the longest line determines the black box 
        

        msg = '%s%s' % ('\033[40m', msg)
        return '%s%s%s' % (RED, msg, _RESET, )

    def format_msg(self, var_name: CellName, stack_trace: Optional[StackSummary] = None) -> StackTrace:
        base_msg = 'Global shared variable < %s > is not supported.' % (var_name, )
        
        if stack_trace is None:
            return base_msg
        
        trace = self.format_exception(stack_trace)
        return '%s\n%s' % (base_msg, trace)


class DuplicateTestFound(Exception):

    def __init__(self, test_names: list[TestFunctionName]) -> None:
        msg = 'Duplicate test(s) found: < %s >' % (', '.join(test_names), )
        super().__init__(msg)
