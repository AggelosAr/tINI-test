import secrets

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



get_registry_key = lambda prefix: '%s_%s' % (prefix, secrets.token_hex(5))

_T_REG = get_registry_key('_TEST_REGISTRY')
_M_REG = get_registry_key('_MOCK_REGISTRY')
_S_REG = get_registry_key('_SHARED_REGISTRY')
_I_REG = get_registry_key('_ISOLATE_REGISTRY')
_C_REG = get_registry_key('_CONNECTION_REGISTRY')
