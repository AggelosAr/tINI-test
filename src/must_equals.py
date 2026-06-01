import difflib
import dis
from functools import lru_cache
from typing import Any, Optional, assert_never

from src._internals.consts import FALSE_LOAD, RETURN, TRUE_LOAD
from src.misc.annotations import Comperator
from src.misc.exceptions import (ComperatorIsNotValid,
                                 ComperatorWasNotProvided,
                                 ExpectedWasDifferentFromActual)

_known_types = set([bool,
                    int,
                    float,
                    str,
                    set,
                    tuple,
                    list,
                    dict])

here = None

# =========================================================
# Public API
# =========================================================

def must_equal(expected: Any, 
               actual: Any, 
               comperator: Optional[Comperator | Any] = None) -> None:
    """
    Assert that expected and actual are equal.

    Primitive values and built-in containers (str, list, tuple, set,
    dict, etc.) are compared recursively and a human-friendly diff is
    produced when a mismatch is found. If provided, the comperator is always used instead of the
    built-in comparison logic. The comperator must return
    ``True`` when the values should be considered equal and
    ``False`` otherwise.
    """
    # format the exception to stop at the user level.
    
    try:

        if comperator:
            _assert_comperator()

        _must_equal(expected=expected,
                    actual=actual, 
                    path='root',
                    comperator=comperator)

    except ExpectedWasDifferentFromActual as e:
        raise ExpectedWasDifferentFromActual(str(e)) from here
    
    except ComperatorWasNotProvided:
        raise ComperatorWasNotProvided from here
    
    except ComperatorIsNotValid as e:
        raise ComperatorIsNotValid(str(e)) from here
    
# =========================================================
# Helpers
# =========================================================

# TODO add test 
@lru_cache(maxsize=None)
def _assert_comperator(comperator: Optional[Comperator | Any] = None) -> None:

    if not callable(comperator):
        raise ComperatorIsNotValid(reason='Comperator is not a function')
    
    if comperator.__code__.co_argcount != 2:
        raise ComperatorIsNotValid(reason='Comperator must accept two items')
    
    if True in comperator.__code__.co_consts or False in comperator.__code__.co_consts:

        data = dis.Bytecode(function).dis().split('\n')
        data = map(lambda l: l.replace(' ', ''), data)
        data = filter(lambda l: l != '', data)

        has_loads = False
        has_loads_idx = -1

        for idx, line in enumerate(data):

            if TRUE_LOAD in line or FALSE_LOAD in line:
                has_loads = True
                continue

            if all([RETURN in line,
                    has_loads,
                    idx-1 == has_loads_idx]):
                return
    
    raise ComperatorIsNotValid


def _raise_diff(msg: str) -> None:
    raise ExpectedWasDifferentFromActual(msg)


def _unified_diff(expected: Any, actual: Any) -> str:
    exp_lines = str(expected).splitlines(keepends=True)
    act_lines = str(actual).splitlines(keepends=True)

    return ''.join(
        difflib.unified_diff(
            exp_lines,
            act_lines,
            fromfile='expected',
            tofile='actual',
        )
    )

# =========================================================
# Core dispatcher
# =========================================================

def _must_equal(expected: Any, 
                actual: Any, 
                path: str,
                comperator: Optional[Comperator] = None) -> None:

    if expected is None and actual is None:
        return

    if type(expected) != type(actual):
        _raise_diff(
            '%s: type mismatch\nexpected: %s\nactual:   %s'
            % (path, type(expected), type(actual), )
        )

    _is_alien = type(expected) not in _known_types

    if _is_alien and not comperator:
        raise ComperatorWasNotProvided

    if type(expected) not in _known_types:
        _diff_alien_primitive(expected, actual, path, comperator)
        return
    
    if isinstance(expected, bool):
        _diff_primitive(expected, actual, path)
        return

    if isinstance(expected, int):
        _diff_primitive(expected, actual, path)
        return

    if isinstance(expected, float):
        _diff_primitive(expected, actual, path)
        return

    if isinstance(expected, str):
        _diff_str(expected, actual, path)
        return
    
    if isinstance(expected, set):
        _diff_set(expected, actual, path)
        return

    if isinstance(expected, tuple):
        _diff_tuple(expected, actual, path)
        return

    if isinstance(expected, list):
        _diff_list(expected, actual, path)
        return

    if isinstance(expected, dict):
        _diff_dict(expected, actual, path)
        return

    assert_never()


# =========================================================
# Primitive types
# =========================================================

def _diff_primitive(expected: Any, actual: Any, path: str) -> None:
    if expected != actual:
        _raise_diff('%s: %r != %r' % (path, expected, actual, ))


def _diff_str(expected: str, actual: str, path: str) -> None:
    if expected == actual:
        return

    diff = _unified_diff(expected, actual)
    _raise_diff('%s:\n%s' % (path, diff, ))


def _diff_alien_primitive(expected: Any, 
                          actual: Any, 
                          path: str,
                          comperator: Comperator) -> None:
    
    if comperator(expected, actual) is False:
        _raise_diff('%s: %r != %r' % (path, expected, actual, ))

# =========================================================
# Containers
# =========================================================


def _diff_set(expected: set[Any], 
              actual: set[Any], 
              path: str) -> None:

    if expected == actual:
        return

    missing = expected - actual
    extra = actual - expected

    _raise_diff(
        '%s: set mismatch\nmissing: %r\nextra: %r'
        % (path, missing, extra)
    )


def _diff_tuple(expected: tuple[Any, ...], 
                actual: tuple[Any, ...], 
                path: str) -> None:

    if len(expected) != len(actual):
        _raise_diff(
            'tuple length mismatch\nexpected=%d actual=%d'
            % (len(expected), len(actual))
        )

    for i, (e, a) in enumerate(zip(expected, actual)):
        _must_equal(e, a, '%s[%d]' % (path, i, ))


def _diff_list(expected: list[Any], 
               actual: list[Any], 
               path: str) -> None:

    if len(expected) != len(actual):
        _raise_diff(
            'list length mismatch\nexpected=%d actual=%d'
            % (len(expected), len(actual))
        )

    for i, (e, a) in enumerate(zip(expected, actual)):
        _must_equal(e, a, '%s[%d]' % (path, i, ))


def _diff_dict(expected: dict[Any, Any], 
               actual: dict[Any, Any], 
               path: str) -> None:

    if expected.keys() != actual.keys():
        missing = expected.keys() - actual.keys()
        extra = actual.keys() - expected.keys()

        _raise_diff(
            '%s: dict key mismatch\nmissing: %r\nextra: %r'
            % (path, missing, extra)
        )

    for key in expected:
        _must_equal(expected[key], actual[key], '%s[%r]' % (path, key, ))
