from tini_test._internals._dynamic_reg_ids import (__C_REG, __I_REG, __M_REG,
                                                   __S_REG, __T_REG)

_RESET = '\033[0m'                   # Reset line colours

_LINE_UP = '\033[1A'                 # Used on minimal dots
_LINE_CLEAR = '\x1b[2K'              # Used on minimal dots

SEPERATOR_LENGTH = 120               # Seperator length
SEPERATOR_SYMBOL = '='               # Seperator symbol
SEPERATOR_NEGATIVE = '\033[7m'       # Seperator start
SEPERATOR_CYAN = '\033[96m'          # Seperator color

INVALID_PYTHON_MODULE_SYMBOLS = set(['.', '/', '\\'])

SKIP_DIRS = {
        '__pycache__',
        '312venv',
        '.venv',
        'venv',
        'env',
        'build',
        'dist',
        '.git',
        '.pytest_cache',
        '.mypy_cache',
        'node_modules',
        'jeepney'
    }


SHARED_ID = 'var'

capture_flag = ('<frozen importlib._bootstrap>', '_call_with_frames_removed', )


_T_REG = __T_REG
_M_REG = __M_REG
_S_REG = __S_REG
_I_REG = __I_REG
_C_REG = __C_REG
