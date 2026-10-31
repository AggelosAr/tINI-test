from __future__ import annotations

import builtins
import inspect
from enum import Enum
from functools import lru_cache
from typing import Any, Mapping

from tini_test.coverage.consts import STORE
from tini_test.misc.exceptions import (NotSupportedRunMode,
                                       NotSupportedVerbosity,
                                       TiniTestInternalException)

from .misc.annotations import ColorValue, MockedRawItem


class TiniTestMode(Enum):
    MERGE           = 'MERGE'
    HTML_REPORT     = 'HTML_REPORT'
    RUN             = 'RUN'



class RunMode(Enum):
    
    SYNC            = 'SYNC'
    ASYNC           = 'ASYNC'

    @classmethod
    def supported_modes_help_msg(cls) -> str:
        return 'Supported run modes are <SYNC> and <ASYNC>'
    
    @classmethod
    def arg_parser_type(cls, value: str) -> RunMode:
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise NotSupportedRunMode(msg=cls.supported_modes_help_msg())

    @classmethod
    def arg_parser_info(cls) -> str:
        return r'''
-Case insensitive. 

Sync ( DEFAULT )
----
Run all tests in sync mode.

Async
-----
Run all tests in async mode.
               '''
    

class Verbosity(Enum):

    NORMAL           = 'NORMAL'
    SORT             = 'SORT'
    MINIMAL          = 'MINIMAL'
    MINIMAL_NO_STACK = 'MINIMAL_NO_STACK'
    SUPER_MINIMAL    = 'SUPER_MINIMAL'

    @classmethod
    def supported_modes_help_msg(cls) -> str:
        modes = ', '.join(member.value for member in cls)
        return 'Supported verbosity modes are <%s>' % (modes, )
    
    @classmethod
    def arg_parser_type(cls, value: str) -> Verbosity:
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise NotSupportedVerbosity(msg=cls.supported_modes_help_msg())

    @classmethod
    def arg_parser_info(cls) -> str:
        return r'''
-Case insensitive.

Normal
------
Full stack trace and print capture with nice borders. Also includes helpful details.

Sort ( DEFAULT )
----
Same as normal but the errors are sorted per module.

minimal
-------
* Failed tests ( names only )
* Associated stack traces
* Final execution summary

minimal_no_stack
----------------
Same as `MINIMAL`, except that no stack traces are shown.

super_minimal
-------------
Same as `MINIMAL_NO_STACK` but less verbose.
               '''


class Coverage(Enum):
    ENABLED     = 'ENABLED'
    DISABLED    = 'DISABLED'

    @classmethod
    def arg_parser_info(cls) -> str:
        return r'''
> Doesn't accept any arguments.

If passed, coverage tracking will be enabled.
The report that will be generated, shows the coverage analysis of the code based on the collected data.
The report will be generated in HTML format and will be stored inside the `%s` directory.
Use --coverage-target and --coverage-store to further configure the behavior of the coverage report.
               ''' % STORE


class ScoreClass(Enum):
    EXCELLENT   = 'EXCELLENT'
    AVERAGE     = 'AVERAGE'
    POOR        = 'POOR'

    @classmethod
    def get_score_category(cls, score: float) -> ScoreClass:
        if score >= 80:
            return ScoreClass.EXCELLENT
        
        if score >= 50:
            return ScoreClass.AVERAGE
        
        return ScoreClass.POOR


class TestStatus(Enum):
    NO_OP = 'NO_OP'

    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'

    SET_UP_ENTRY = 'SET_UP_ENTRY'
    SET_UP_SUCCESS = 'SET_UP_SUCCESS'
    SET_UP_FAIL = 'SET_UP_FAIL'
    
    BREAK_DOWN_ENTRY = 'BREAK_DOWN_ENTRY'
    BREAK_DOWN_SUCCESS = 'BREAK_DOWN_SUCCESS'
    BREAK_DOWN_FAIL = 'BREAK_DOWN_FAIL'

    ATTEMPT_BREAK_DOWN_ENTRY_FROM_SETUP_FAIL = 'ATTEMPT_BREAK_DOWN_ENTRY_FROM_SETUP_FAIL'
    ATTEMPT_BREAK_DOWN_ENTRY_FROM_FAIL = 'ATTEMPT_BREAK_DOWN_ENTRY_FROM_FAIL'
    ATTEMPT_BREAK_DOWN_SUCCESS = 'ATTEMPT_BREAK_DOWN_SUCCESS'
    ATTEMPT_BREAK_DOWN_FAIL = 'ATTEMPT_BREAK_DOWN_FAIL'

    # MUST_EQUALS_DIFF = 'MUST_EQUALS_DIFF' # not implemented
    
    @classmethod
    @lru_cache
    def fail_operations(cls) -> set[TestStatus]:
        return set([cls.FAIL,
                    cls.SET_UP_FAIL, 
                    cls.BREAK_DOWN_FAIL,
                    cls.ATTEMPT_BREAK_DOWN_ENTRY_FROM_SETUP_FAIL,
                    cls.ATTEMPT_BREAK_DOWN_ENTRY_FROM_FAIL,
                    cls.ATTEMPT_BREAK_DOWN_SUCCESS,
                    cls.ATTEMPT_BREAK_DOWN_FAIL]) 
    
    @classmethod
    @lru_cache
    def is_fail_cause(cls, status: TestStatus) -> bool:
        return status in cls.fail_operations()


class Plugs(Enum):
    TEST        = 'TEST'
    MOCK        = 'MOCK'
    SHARED      = 'SHARED'
    ISOLATE     = 'ISOLATE'


class MockType(Enum):
    BUILTIN     = 'BUILTIN'
    CLASS       = 'CLASS'
    FUNCTION    = 'FUNCTION'

    @classmethod
    def get_type(cls, mock: Any) -> tuple[MockType, MockedRawItem]:
        try:
            # Builtin method
            if inspect.isbuiltin(mock):
                return MockType.BUILTIN, mock

            # Builtin class/type
            if getattr(builtins, mock.__name__, None):
                return MockType.BUILTIN, mock
            
            if inspect.isclass(mock):
                return MockType.CLASS, mock
            
            if callable(mock):
                return MockType.FUNCTION, mock
            
        except Exception as e:
            raise TiniTestInternalException('Unsupported mock type') from e

        raise TiniTestInternalException('Unsupported mock type')    # >>> assert missing


class Color(Enum):
    RED         = '\033[91m'     
    DARK_RED    = '\033[31m'

    GREEN       = '\033[92m'
    DARK_GREEN  = '\033[32m'

    YELLOW      = '\033[93m'
    BLUE        = '\033[94m'
    MAGENTA     = '\033[95m'
    WHITE       = '\033[97m'

    ORANGE      = '\033[38;5;208m'
    DARK_ORANGE = '\033[38;5;166m'


CONFIG: Mapping[TestStatus, ColorValue] = {
    TestStatus.SUCCESS: Color.GREEN.value,
    TestStatus.FAIL: Color.RED.value,
    TestStatus.SET_UP_ENTRY: Color.BLUE.value,
    TestStatus.SET_UP_SUCCESS: Color.BLUE.value,
    TestStatus.SET_UP_FAIL: Color.YELLOW.value,
    TestStatus.BREAK_DOWN_ENTRY: Color.BLUE.value,
    TestStatus.BREAK_DOWN_SUCCESS: Color.BLUE.value,
    TestStatus.BREAK_DOWN_FAIL: Color.YELLOW.value,
    TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_SETUP_FAIL: Color.MAGENTA.value,
    TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_FAIL: Color.MAGENTA.value,
    TestStatus.ATTEMPT_BREAK_DOWN_SUCCESS: Color.MAGENTA.value,
    TestStatus.ATTEMPT_BREAK_DOWN_FAIL: Color.MAGENTA.value,
}
