from enum import Enum


class Config(Enum):

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = "\033[96m"

    NEGATIVE = "\033[7m"
    RESET = '\033[0m'

    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'


class Mode(Enum):
    
    NORMAL = 'NORMAL'
    SORT = 'SORT'
    MINIMAL = 'MINIMAL'

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

    # TODO unused maybe update?
    @classmethod
    def continue_operations(cls) -> set['TestStatus']:
        1/0
        return set([cls.NO_OP, 
                    cls.SUCCESS, 
                    cls.SET_UP_SUCCESS,
                    cls.BREAK_DOWN_SUCCESS])

    @classmethod
    def abort_operations(cls) -> set['TestStatus']:
        return set([cls.FAIL, 
                    cls.SET_UP_FAIL, 
                    cls.BREAK_DOWN_FAIL])
    
    # TODO OPT cache this
    @classmethod
    def is_abort_cause(cls, status: 'TestStatus') -> bool:
        return status in cls.abort_operations()
