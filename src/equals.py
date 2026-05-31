from difflib import unified_diff
from typing import Any

from misc.equal_exceptions import (DictionaryMismatchError,
                                   DictionarySizeMismatchError,
                                   FloatMismatchError, IntegerMismatchError,
                                   ListMismatchError, ListSizeMismatchError,
                                   StringMismatchError, TypeMismatchError)


def must_not_equal(a, b):
    return not a == b


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
    ...


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
    ...


def compare_dict(a: dict[Any, Any], b: dict[Any, Any]) -> None:
    if a.keys() != b.keys():
        raise DictionarySizeMismatchError(a, b, "key mismatch")

    for k in a:
        if a[k] != b[k]:
            raise DictionaryMismatchError(
                a,
                b,
                "value mismatch at key %s: %s != %s" % (k, a[k], b[k])
            )






def must_equal(a: Any, b: Any) -> None:
    if type(a) != type(b):
        type_mismatch(a, b)

    _type = type(a)

    match _type:

        case int():
            compare_int(a, b)

        case float():
            compare_float(a, b)

        case str():
            compare_str(a, b)

        case tuple():
            compare_tuple(a, b)

        case list():
            compare_list(a, b)

        case set():
            compare_set(a, b)

        case dict():
            compare_dict(a, b)

        case _:
            NotImplementedError


must_equal('a','a')
