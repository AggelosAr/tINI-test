from enum import Enum


class Config(Enum):

    RED = '\033[91m'         # FAIL
    GREEN = '\033[92m'       # SUCCESS
    YELLOW = '\033[93m'      # SET_UP_FAIL | BREAK_DOWN_FAIL | ATTEMPT_BREAK_DOWN_FAIL
    BLUE = '\033[94m'        # SET_UP_ENTRY | SET_UP_SUCCESS | BREAK_DOWN_ENTRY | BREAK_DOWN_SUCCESS
    MAGENTA = '\033[95m'     # ALL ATTEMPTs

    NEGATIVE = "\033[7m"     # Negative

    LINE_UP = '\033[1A'      # Used on minimal dots
    LINE_CLEAR = '\x1b[2K'   # Used on minimal dots

    CYAN = "\033[96m"        # Seperator
    SEPERATOR_LENGTH = 120   # Seperator length
    SEPERATOR_SYMBOL = '='   # Seperator symbol


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
    def fail_operations(cls) -> set['TestStatus']:
        return set([cls.FAIL,
                    cls.SET_UP_FAIL, 
                    cls.BREAK_DOWN_FAIL,
                    cls.ATTEMPT_BREAK_DOWN_ENTRY_FROM_SETUP_FAIL,
                    cls.ATTEMPT_BREAK_DOWN_ENTRY_FROM_FAIL,
                    cls.ATTEMPT_BREAK_DOWN_SUCCESS,
                    cls.ATTEMPT_BREAK_DOWN_FAIL]) 
    
    @classmethod
    def is_fail_cause(cls, status: 'TestStatus') -> bool:
        return status in cls.fail_operations()
