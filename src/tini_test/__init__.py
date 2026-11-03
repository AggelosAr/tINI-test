from ._internals._isolate import Isolate
from .context_managers import WillRaise
from .context_managers import _CX_Mocking as _Mocking
from .misc.exceptions import ExpectedWasDifferentFromActual
from .mock import Mock as _Mock
from .must_equals import must_equal
from .shared import NotInitialized, Shared, var
from .test_utils import Test

__version__ = '0.9.5'


class Mock(_Mock, _Mocking): ...

__all__ = [
    'Test',
    'WillRaise',
    'ExpectedWasDifferentFromActual',
    'must_equal',
    'Mock',
    'Shared',
    'var',
    'NotInitialized',
    'Isolate',
    '__version__',
]
