from difflib import unified_diff
from typing import Any

from src._internals._internal_exceptions._comparison_exceptions import (
    _BoolMismatchError, _DictionaryKeysMismatchError, _DictionaryMismatchError,
    _DictionarySizeMismatchError, _FloatMismatchError, _IntegerMismatchError,
    _ListMismatchError, _ListSizeMismatchError, _SetMismatchError,
    _SetSizeMismatchError, _StringMismatchError, _TupleMismatchError,
    _TupleSizeMismatchError, _TypeMismatchError)

# TODO add custom comperator 


def _must_equal(a: Any, b: Any) -> None:

    if a is None and b is None:
        return
    
    if a is None or b is None and not (a is None and b is None):
        raise _TypeMismatchError(a, b)
    
    if type(a) != type(b):
        _type_mismatch(a, b)

    match type(a).__name__:
        
        case bool.__name__:
            _compare_bool(a, b)

        case int.__name__:
            _compare_int(a, b)

        case float.__name__:
            _compare_float(a, b)

        case str.__name__:
            _compare_str(a, b)

        case tuple.__name__:
            _compare_tuple(a, b)

        case list.__name__:
            _compare_list(a, b)

        case set.__name__:
            _compare_set(a, b)

        case dict.__name__:
            _compare_dict(a, b)

        case _:
            raise NotImplementedError


def _type_mismatch(a: Any, b: Any) -> None:
    raise _TypeMismatchError(a, b)


def _compare_bool(a: bool, b: bool) -> None:
    if a != b:
        raise _BoolMismatchError(a, b)
    

def _compare_int(a: int, b: int) -> None:
    if a != b:
        raise _IntegerMismatchError(a, b)


def _compare_float(a: float, b: float) -> None:
    if a != b:
        raise _FloatMismatchError(a, b)
    

def _compare_str(a: str, b: str) -> None:
    if a != b:
        raise _StringMismatchError(a, b)


def _compare_tuple(a: tuple[Any], b: tuple[Any]) -> None:

    if len(a) != len(b):
        raise _TupleSizeMismatchError(
            a,
            b,
            'tuple size mismatch'
        )

    for i, (left, right) in enumerate(zip(a, b)):

        if left != right:
            raise _TupleMismatchError(
                a,
                b,
                'element mismatch at index %s: %s != %s' % (
                    i,
                    left,
                    right,
                )
            )


def _compare_list(a: list[Any], b: list[Any]) -> None:
    if len(a) != len(b):
        raise _ListSizeMismatchError(a, b, 'length mismatch')

    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            raise _ListMismatchError(
                a,
                b,
                'element mismatch at index %s: %s != %s' % (i, x, y, )
            )


def _compare_set(a: set[Any], b: set[Any]) -> None:

    if len(a) != len(b):
        raise _SetSizeMismatchError(
            a,
            b,
            'set size mismatch'
        )

    missing = a - b
    extra = b - a

    if missing or extra:
        raise _SetMismatchError(
            a,
            b,
            'missing=%s extra=%s' % (
                missing,
                extra,
            )
        )


def _compare_dict(a: dict[Any, Any], b: dict[Any, Any]) -> None:

    if len(a) != len(b):
        raise _DictionarySizeMismatchError(a, b, 'size mismatch')
    
    if a.keys() != b.keys():
        raise _DictionaryKeysMismatchError(a, b, 'key mismatch')
    
    for k in a:
        if a[k] != b[k]:
            raise _DictionaryMismatchError(
                a,
                b,
                'value mismatch at key %s: %s != %s' % (k, a[k], b[k], )
            )
