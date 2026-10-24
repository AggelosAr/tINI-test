from ._internals._isolate import Isolate
from .context_managers import Mock as _Mocking
from .context_managers import WillRaise
from .misc.exceptions import ExpectedWasDifferentFromActual
from .mock import Mock as _Mock
from .must_equals import must_equal
from .shared import NotInitialized, Shared, var
from .test_utils import Test


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
]
