from src.asserts import WillRaise
from src.equals import must_equal
from src.misc.equal_exceptions import (DictionaryMismatchError,
                                       DictionarySizeMismatchError,
                                       SetSizeMismatchError, SetMismatchError,
                                       FloatMismatchError,
                                       IntegerMismatchError, ListMismatchError,
                                       ListSizeMismatchError,
                                       TupleMismatchError,
                                       TupleSizeMismatchError,
                                       TypeMismatchError)
from src.test_utils import Test



#####################
### NONE
#####################


@Test.case
def test_none_match() -> None:
    a = None
    b = None
    must_equal(a, b)


#####################
### INTS
#####################


@Test.case
def test_ints_match() -> None:
    a = 10
    b = 10
    must_equal(a, b)


@Test.case
def test_ints_dont_match() -> None:
    a = 10
    b = 20

    with WillRaise(IntegerMismatchError):
        must_equal(a, b)


#####################
### FLOATS
#####################


@Test.case
def test_floats_match() -> None:
    a = 3.14
    b = 3.14
    must_equal(a, b)


@Test.case
def test_floats_dont_match() -> None:
    a = 3.14
    b = 2.71

    with WillRaise(FloatMismatchError):
        must_equal(a, b)


@Test.case
def test_float_precision() -> None:
    a = 0.1 + 0.2
    b = 0.3

    with WillRaise(FloatMismatchError):
        must_equal(a, b)


#####################
### BOOLS
#####################


@Test.case
def test_bool_match() -> None:
    a = True
    b = True
    must_equal(a, b)


@Test.case
def test_bool_dont_match() -> None:
    a = True
    b = False

    with WillRaise(IntegerMismatchError):  # bool is subclass of int
        must_equal(a, b)


#####################
### TUPLES
#####################


@Test.case
def test_tuple_match() -> None:
    a = (1, 2, 3)
    b = (1, 2, 3)
    must_equal(a, b)


@Test.case
def test_tuple_dont_match() -> None:
    a = (1, 2, 3)
    b = (1, 2, 9)

    with WillRaise(TupleSizeMismatchError):
        must_equal(a, b)



@Test.case
def test_tuple_dont_match() -> None:
    a = (1, 2, 3)
    b = (1, 2, 9)

    with WillRaise(TupleMismatchError):
        must_equal(a, b)


#####################
### LISTS
#####################


@Test.case
def test_empty_list() -> None:
    must_equal([], [])


@Test.case
def test_list_match() -> None:
    a = [1, 2, 3]
    b = [1, 2, 3]
    must_equal(a, b)


@Test.case
def test_list_size_mismatch() -> None:
    a = [1, 2, 3]
    b = [1, 2]

    with WillRaise(ListSizeMismatchError):
        must_equal(a, b)


@Test.case
def test_list_value_dont_match() -> None:
    a = [1, 2, 3]
    b = [1, 2, 4]

    with WillRaise(ListMismatchError):
        must_equal(a, b)


@Test.case
def test_nested_list_mismatch() -> None:
    a = [1, [2, 3], 4]
    b = [1, [2, 99], 4]

    with WillRaise(ListMismatchError):
        must_equal(a, b)


#####################
### SETS
#####################


@Test.case
def test_set_match() -> None:
    a = {1, 2, 3}
    b = {1, 2, 3}
    must_equal(a, b)


@Test.case
def test_set_dont_match() -> None:
    a = {1, 2, 3}
    b = {1, 2, 4, 6}

    with WillRaise(SetSizeMismatchError):
        must_equal(a, b)


@Test.case
def test_set_dont_match() -> None:
    a = {1, 2, 3}
    b = {1, 2, 4}

    with WillRaise(SetMismatchError):
        must_equal(a, b)


#####################
### DICTS
#####################


@Test.case
def test_empty_dict() -> None:
    must_equal({}, {})


@Test.case
def test_dict_match() -> None:
    a = {"x": 1, "y": 2}
    b = {"x": 1, "y": 2}
    must_equal(a, b)


@Test.case
def test_dict_key_mismatch() -> None:
    a = {"x": 1, "y": 2}
    b = {"x": 1, "z": 2}

    with WillRaise(DictionarySizeMismatchError):
        must_equal(a, b)


@Test.case
def test_dict_value_mismatch() -> None:
    a = {"x": 1, "y": 2}
    b = {"x": 1, "y": 3}

    with WillRaise(DictionaryMismatchError):
        must_equal(a, b)


@Test.case
def test_nested_dict() -> None:
    a = {"a": {"b": {"c": 1}}}
    b = {"a": {"b": {"c": 2}}}

    with WillRaise(DictionaryMismatchError):
        must_equal(a, b)



#####################
### MISC
#####################


@Test.case
def test_type_mismatch_int_str() -> None:
    a = 10
    b = "10"

    with WillRaise(TypeMismatchError):
        must_equal(a, b)


@Test.case
def test_none_vs_int() -> None:
    with WillRaise(TypeMismatchError):
        must_equal(None, 1)

