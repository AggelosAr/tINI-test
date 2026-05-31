from typing import Any

from src.misc.annotations import DiffMessage


class MustEqualError(Exception):
    '''Base exception for all must_equal failures.'''
    def __init__(self, message: DiffMessage):
        super().__init__(message)
        # self.message = message


class TypeMismatchError(MustEqualError):

    def __init__(self, a: Any, b: Any):
        msg = 'Expected type <%s> is different from <%s>' % (
            type(a).__name__,
            type(b).__name__
        )
        super().__init__(msg)


class BoolMismatchError(MustEqualError):

    def __init__(self, a: bool, b: bool) -> None:
        msg = '%s != %s' % (a, b, )
        super().__init__(msg)


class IntegerMismatchError(MustEqualError):

    def __init__(self, a: int, b: int) -> None:
        msg = '%s != %s' % (a, b, )
        super().__init__(msg)


class FloatMismatchError(MustEqualError):

    def __init__(self, a: float, b: float) -> None:
        msg = '%s != %s' % (a, b, )
        super().__init__(msg)


class StringMismatchError(MustEqualError):

    def __init__(self, a: str, b: str) -> None:
        msg = '%s != %s' % (a, b, )
        super().__init__(msg)


class TupleSizeMismatchError(MustEqualError):

    def __init__(self, a: list[Any], b: list[Any], detail='') -> None:
        msg = '%s != %s | %s' % (len(a), len(b), detail, )
        super().__init__(msg)


class TupleMismatchError(MustEqualError):

    def __init__(self, a: tuple[Any], b: tuple[Any], detail='') -> None:
        msg = '%s != %s | %s' % (a, b, detail, )
        super().__init__(msg)


class ListSizeMismatchError(MustEqualError):

    def __init__(self, a: list[Any], b: list[Any], detail='') -> None:
        msg = '%s != %s | %s' % (len(a), len(b), detail, )
        super().__init__(msg)


class ListMismatchError(MustEqualError):

    def __init__(self, a: list[Any], b: list[Any], detail='') -> None:
        msg = '%s != %s | %s' % (a, b, detail, )
        super().__init__(msg)


class SetSizeMismatchError(MustEqualError):

    def __init__(self, a: set[Any], b: set[Any], detail='') -> None:
        msg = '%s != %s | %s' % (len(a), len(b), detail, )
        super().__init__(msg)


class SetMismatchError(MustEqualError):

    def __init__(self, a: set[Any], b: set[Any], detail='') -> None:
        msg = '%s != %s | %s' % (a, b, detail, )
        super().__init__(msg)


class DictionarySizeMismatchError(MustEqualError):

    def __init__(self, a: dict[Any, Any], b: dict[Any, Any], detail='') -> None:
        msg = '%s != %s | %s' % (len(a), len(b), detail, )
        super().__init__(msg)


class DictionaryKeysMismatchError(MustEqualError):

    def __init__(self, a: dict[Any, Any], b: dict[Any, Any], detail='') -> None:
        msg = '%s != %s | %s' % (sorted(a.keys()), sorted(b.keys()), detail, )
        super().__init__(msg)


class DictionaryMismatchError(MustEqualError):

    def __init__(self, a: dict[Any, Any], b: dict[Any, Any], detail='') -> None:
        msg = '%s != %s | %s' % (a, b, detail, )
        super().__init__(msg)
