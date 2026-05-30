from enum import Enum


class Config(Enum):

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = "\033[96m"
    MAGENTA = '\033[95m'

    NEGATIVE = "\033[7m"
    RESET = '\033[0m'

    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'


class Mode(Enum):
    
    NORMAL = 'NORMAL'
    SORT = 'SORT'
    MINIMAL = 'MINIMAL'
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
    def fail_operations(cls) -> set['TestStatus']:
        return set([cls.FAIL,
                    cls.SET_UP_FAIL, 
                    cls.BREAK_DOWN_FAIL,
                    cls.ATTEMPT_BREAK_DOWN_ENTRY_FROM_SETUP_FAIL,
                    cls.ATTEMPT_BREAK_DOWN_ENTRY_FROM_FAIL,
                    cls.ATTEMPT_BREAK_DOWN_SUCCESS,
                    cls.ATTEMPT_BREAK_DOWN_FAIL]) 
    
    @classmethod
    def is_abort_cause(cls, status: 'TestStatus') -> bool:
        return status in cls.fail_operations()
    
    @classmethod
    def is_fail_cause(cls, status: 'TestStatus') -> bool:
        return status in cls.fail_operations()
