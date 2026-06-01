from typing import Any

from src.misc.annotations import DiffMessage


class _MustEqualError(Exception):
    '''Base exception for all must_equal failures.'''
    def __init__(self, message: DiffMessage):
        super().__init__(message)
        # self.message = message


class _TypeMismatchError(_MustEqualError):

    def __init__(self, a: Any, b: Any):
        msg = 'Expected type <%s> is different from <%s>' % (
            type(a).__name__,
            type(b).__name__
        )
        super().__init__(msg)


class _BoolMismatchError(_MustEqualError):

    def __init__(self, a: bool, b: bool) -> None:
        msg = '%s != %s' % (a, b, )
        super().__init__(msg)


class _IntegerMismatchError(_MustEqualError):

    def __init__(self, a: int, b: int) -> None:
        msg = '%s != %s' % (a, b, )
        super().__init__(msg)


class _FloatMismatchError(_MustEqualError):

    def __init__(self, a: float, b: float) -> None:
        msg = '%s != %s' % (a, b, )
        super().__init__(msg)


class _StringMismatchError(_MustEqualError):

    def __init__(self, a: str, b: str) -> None:
        msg = '%s != %s' % (a, b, )
        super().__init__(msg)


class _TupleSizeMismatchError(_MustEqualError):

    def __init__(self, a: tuple[Any], b: tuple[Any], detail='') -> None:
        msg = '%s != %s | %s' % (len(a), len(b), detail, )
        super().__init__(msg)


class _TupleMismatchError(_MustEqualError):

    def __init__(self, a: tuple[Any], b: tuple[Any], detail='') -> None:
        msg = '%s != %s | %s' % (a, b, detail, )
        super().__init__(msg)


class _ListSizeMismatchError(_MustEqualError):

    def __init__(self, a: list[Any], b: list[Any], detail='') -> None:
        msg = '%s != %s | %s' % (len(a), len(b), detail, )
        super().__init__(msg)


class _ListMismatchError(_MustEqualError):

    def __init__(self, a: list[Any], b: list[Any], detail='') -> None:
        msg = '%s != %s | %s' % (a, b, detail, )
        super().__init__(msg)


class _SetSizeMismatchError(_MustEqualError):

    def __init__(self, a: set[Any], b: set[Any], detail='') -> None:
        msg = '%s != %s | %s' % (len(a), len(b), detail, )
        super().__init__(msg)


class _SetMismatchError(_MustEqualError):

    def __init__(self, a: set[Any], b: set[Any], detail='') -> None:
        msg = '%s != %s | %s' % (a, b, detail, )
        super().__init__(msg)


class _DictionarySizeMismatchError(_MustEqualError):

    def __init__(self, a: dict[Any, Any], b: dict[Any, Any], detail='') -> None:
        msg = '%s != %s | %s' % (len(a), len(b), detail, )
        super().__init__(msg)


class _DictionaryMismatchError(_MustEqualError):

    def __init__(self, a: dict[Any, Any], b: dict[Any, Any], detail='') -> None:
        msg = '%s != %s | %s' % (a, b, detail, )
        super().__init__(msg)
