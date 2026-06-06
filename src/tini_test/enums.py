from enum import Enum
from functools import lru_cache
from typing import Mapping

from tini_test.misc.exceptions import (NotSupportedRunMode,
                                       NotSupportedVerbosity)

from .misc.annotations import ColorValue


class RunMode(Enum):
    
    SYNC = 'SYNC'
    ASYNC = 'ASYNC'

    @classmethod
    def supported_modes_help_msg(cls) -> str:
        modes = ', '.join(member.value for member in cls)
        return 'Supported run modes are <%s>\n' % (modes, )
    
    @classmethod
    def arg_parser_type(cls, value: str) -> 'RunMode':
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise NotSupportedRunMode(msg=cls.supported_modes_help_msg())


class Verbosity(Enum):
    
    SORT = 'SORT'
    NORMAL = 'NORMAL'
    MINIMAL = 'MINIMAL'
    SUPER_MINIMAL = 'SUPER_MINIMAL'
    MINIMAL_NO_STACK = 'MINIMAL_NO_STACK'

    @classmethod
    def supported_modes_help_msg(cls) -> str:
        modes = ', '.join(member.value for member in cls)
        return 'Supported verbosity modes are <%s>' % (modes, )
    
    @classmethod
    def arg_parser_type(cls, value: str) -> 'Verbosity':
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise NotSupportedVerbosity(msg=cls.supported_modes_help_msg())


class Color(Enum):

    RED = '\033[91m'     
    #RED = "\x1b[103m"

    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'


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
    def fail_operations(cls) -> set['TestStatus']:
        return set([cls.FAIL,
                    cls.SET_UP_FAIL, 
                    cls.BREAK_DOWN_FAIL,
                    cls.ATTEMPT_BREAK_DOWN_ENTRY_FROM_SETUP_FAIL,
                    cls.ATTEMPT_BREAK_DOWN_ENTRY_FROM_FAIL,
                    cls.ATTEMPT_BREAK_DOWN_SUCCESS,
                    cls.ATTEMPT_BREAK_DOWN_FAIL]) 
    
    @classmethod
    @lru_cache
    def is_fail_cause(cls, status: 'TestStatus') -> bool:
        return status in cls.fail_operations()


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
