import difflib
from typing import Any

from src.misc.exceptions import (ExpectedWasDifferentFromActual,
                                 MustEqualReceivedNotKnownTypes)

# =========================================================
# Public API
# =========================================================

def must_equal(expected: Any, actual: Any) -> None:
    
    try:
        _must_equal(expected, actual, path='root')
    except ExpectedWasDifferentFromActual as e:
         # format the exception to stop at the user level.
         raise ExpectedWasDifferentFromActual(str(e))
    
# =========================================================
# Helpers
# =========================================================

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

def _must_equal(expected: Any, actual: Any, path: str) -> None:

    if expected is None and actual is None:
        return

    if type(expected) != type(actual):
        _raise_diff(
            '%s: type mismatch\nexpected: %s\nactual:   %s'
            % (path, type(expected), type(actual), )
        )

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

    if isinstance(expected, tuple):
        _diff_tuple(expected, actual, path)
        return

    if isinstance(expected, list):
        _diff_list(expected, actual, path)
        return

    if isinstance(expected, set):
        _diff_set(expected, actual, path)
        return

    if isinstance(expected, dict):
        _diff_dict(expected, actual, path)
        return

    raise MustEqualReceivedNotKnownTypes(type(expected), type(actual))


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


# =========================================================
# Containers
# =========================================================

def _diff_list(expected: list[Any], actual: list[Any], path: str) -> None:

    if len(expected) != len(actual):
        _raise_diff(
            '%s: list length mismatch\nexpected=%d actual=%d'
            % (path, len(expected), len(actual))
        )

    for i, (e, a) in enumerate(zip(expected, actual)):
        _must_equal(e, a, '%s[%d]' % (path, i))


def _diff_tuple(expected: tuple[Any, ...], actual: tuple[Any, ...], path: str) -> None:

    if len(expected) != len(actual):
        _raise_diff(
            '%s: tuple length mismatch\nexpected=%d actual=%d'
            % (path, len(expected), len(actual))
        )

    for i, (e, a) in enumerate(zip(expected, actual)):
        _must_equal(e, a, '%s[%d]' % (path, i))


def _diff_set(expected: set[Any], actual: set[Any], path: str) -> None:

    if expected == actual:
        return

    missing = expected - actual
    extra = actual - expected

    _raise_diff(
        '%s: set mismatch\nmissing: %r\nextra: %r'
        % (path, missing, extra)
    )


def _diff_dict(expected: dict[Any, Any], actual: dict[Any, Any], path: str) -> None:

    if expected.keys() != actual.keys():
        missing = expected.keys() - actual.keys()
        extra = actual.keys() - expected.keys()

        _raise_diff(
            '%s: dict key mismatch\nmissing: %r\nextra: %r'
            % (path, missing, extra)
        )

    for key in expected:
        _must_equal(
            expected[key],
            actual[key],
            '%s[%r]' % (path, key)
        )