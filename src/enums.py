from enum import Enum
from functools import lru_cache
from typing import Mapping


class Color(Enum):

    RED = '\033[91m'        
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'


class Mode(Enum):
    
    SORT = 'SORT'
    NORMAL = 'NORMAL'
    MINIMAL = 'MINIMAL'
    SUPER_MINIMAL = 'SUPER_MINIMAL'
    MINIMAL_NO_STACK = 'MINIMAL_NO_STACK'

    @classmethod
    def supported_modes(cls) -> str:
        modes = ', '.join(member.value for member in cls)
        return 'Supported modes are <%s>' % (modes, )


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


CONFIG: Mapping[TestStatus, Color] = {
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
