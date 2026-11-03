from dataclasses import dataclass
from pathlib import Path

from tini_test._internals._dynamic_reg_ids import (__C_REG, __I_REG, __M_REG,
                                                   __R_M_REG, __R_T_REG,
                                                   __S_REG, __T_REG)
from tini_test.misc.annotations import HexStr, DirectoryPath

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


@dataclass(frozen=True)
class Init:
    _ROOT           : DirectoryPath
    _ANCHOR_FRAME   : HexStr

_INIT: list[Init] = []



HEALTH_URL = 'http://127.0.0.1:8000/'


COVERAGE_ROOT        = '/tmp/coverages/tini_test/'
GENERATED_TESTS_ROOT = '/tmp/python/tini_test'


# If we are running the Coverage in V2 mode
# ** Assumes all tests are passing **
# Used to track coverage over coverage
_V2_COVERAGE    = True # True
_USING_COVERAGE = True # True

_PROFILING      = False


_RESET             = '\033[0m'       # Reset line colours

_LINE_UP           = '\033[1A'       # Used on minimal dots
_LINE_CLEAR        = '\x1b[2K'       # Used on minimal dots

SEPERATOR_LENGTH   = 120             # Seperator length
SEPERATOR_SYMBOL   = '='             # Seperator symbol
SEPERATOR_NEGATIVE = '\033[7m'       # Seperator start
SEPERATOR_CYAN     = '\033[96m'      # Seperator color


INVALID_PYTHON_MODULE_SYMBOLS = frozenset(['.', '/', '\\'])

SKIP_DIRS = frozenset({
        '__pycache__',
        '.venv',
        'venv',
        'env',
        'build',
        'dist',
        '.git',
        '.pytest_cache',
        '.mypy_cache',
        'node_modules',
    })


capture_flag = ('<frozen importlib._bootstrap>', '_call_with_frames_removed', )

SALT = 5


# Unresolved Registries
_T_REG = __T_REG(SALT)
_M_REG = __M_REG(SALT)
_S_REG = __S_REG(SALT)
_I_REG = __I_REG(SALT)
_C_REG = __C_REG(SALT)


# Resolved Registries
_R_M_REG = __R_M_REG(SALT)
_R_T_REG = __R_T_REG(SALT)


_I_DEC = ('_XMock.mock', '_XTest.test', '_XShared.shared', '_XIsolate.isolate') # XXX remove magic strings.
E_DEC  = frozenset({'Test.case', 'Mock.mock', 'Shared', 'Isolate'})



_SETNINEL = object
_ROOT_SENTINEL = object()
