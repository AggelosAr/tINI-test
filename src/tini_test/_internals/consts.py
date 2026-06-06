
_RESET = '\033[0m'                   # Reset line colours

_LINE_UP = '\033[1A'                 # Used on minimal dots
_LINE_CLEAR = '\x1b[2K'              # Used on minimal dots

SEPERATOR_LENGTH = 120               # Seperator length
SEPERATOR_SYMBOL = '='               # Seperator symbol
SEPERATOR_NEGATIVE = "\033[7m"       # Seperator start
SEPERATOR_CYAN = "\033[96m"          # Seperator color

INVALID_PYTHON_MODULE_SYMBOLS = set(['.', '/', '\\'])

SKIP_DIRS = {
        "__pycache__",
        ".venv",
        "venv",
        "env",
        "build",
        "dist",
        ".git",
        ".pytest_cache",
        ".mypy_cache",
        "node_modules"
    }
