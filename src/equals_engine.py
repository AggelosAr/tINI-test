from difflib import unified_diff
from typing import Any

from src.misc._internal_exceptions.comparison_exceptions import (
    BoolMismatchError, DictionaryKeysMismatchError, DictionaryMismatchError,
    DictionarySizeMismatchError, FloatMismatchError, IntegerMismatchError,
    ListMismatchError, ListSizeMismatchError, SetMismatchError,
    SetSizeMismatchError, StringMismatchError, TupleMismatchError,
    TupleSizeMismatchError, TypeMismatchError)

# TODO add custom comperator 


def must_equal(a: Any, b: Any) -> None:

    if a is None and b is None:
        return
    
    if a is None or b is None and not (a is None and b is None):
        raise TypeMismatchError(a, b)
    
    if type(a) != type(b):
        type_mismatch(a, b)

    print('-------------------')


    print('COMPARING -> ', a, b, )
    print('COMPARING -> ', type(a), type(b), )
    print('-------------------')

    match type(a).__name__:
        
        case bool.__name__:
            compare_bool(a, b)

        case int.__name__:
            compare_int(a, b)

        case float.__name__:
            compare_float(a, b)

        case str.__name__:
            compare_str(a, b)

        case tuple.__name__:
            compare_tuple(a, b)

        case list.__name__:
            compare_list(a, b)

        case set.__name__:
            compare_set(a, b)

        case dict.__name__:
            compare_dict(a, b)

        case _:
            raise NotImplementedError


def _safe_diff(a, b):
    """
    Placeholder for difflib integration.

    You may later replace this with:
        import difflib
        difflib.ndiff(...)
    """
    return "diff-not-implemented"


def type_mismatch(a: Any, b: Any) -> None:
    raise TypeMismatchError(a, b)


def compare_bool(a: bool, b: bool) -> None:
    if a != b:
        raise BoolMismatchError(a, b)
    

def compare_int(a: int, b: int) -> None:
    if a != b:
        raise IntegerMismatchError(a, b)


def compare_float(a: float, b: float) -> None:
    if a != b:
        raise FloatMismatchError(a, b)
    

def compare_str(a: str, b: str) -> None:
    if a != b:
        diff = _safe_diff(a, b)
        raise StringMismatchError(a, b)


def compare_tuple(a: tuple[Any], b: tuple[Any]) -> None:

    if len(a) != len(b):
        raise TupleSizeMismatchError(
            a,
            b,
            'tuple size mismatch'
        )

    for i, (left, right) in enumerate(zip(a, b)):

        if left != right:
            raise TupleMismatchError(
                a,
                b,
                'element mismatch at index %s: %s != %s' % (
                    i,
                    left,
                    right,
                )
            )


def compare_list(a: list[Any], b: list[Any]) -> None:
    if len(a) != len(b):
        raise ListSizeMismatchError(a, b, "length mismatch")

    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            raise ListMismatchError(
                a,
                b,
                "element mismatch at index %s: %s != %s" % (i, x, y)
            )


def compare_set(a: set[Any], b: set[Any]) -> None:

    if len(a) != len(b):
        raise SetSizeMismatchError(
            a,
            b,
            'set size mismatch'
        )

    missing = a - b
    extra = b - a

    if missing or extra:
        raise SetMismatchError(
            a,
            b,
            'missing=%s extra=%s' % (
                missing,
                extra,
            )
        )


def compare_dict(a: dict[Any, Any], b: dict[Any, Any]) -> None:

    if len(a) != len(b):
        raise DictionarySizeMismatchError(a, b, "size mismatch")
    
    if a.keys() != b.keys():
        raise DictionaryKeysMismatchError(a, b, "key mismatch")
    
    for k in a:
        if a[k] != b[k]:
            raise DictionaryMismatchError(
                a,
                b,
                "value mismatch at key %s: %s != %s" % (k, a[k], b[k])
            )

#?
def must_not_equal(a, b):
    return not a == b

