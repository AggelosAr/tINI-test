from src.context_manager import WillRaise
from src.equals_engine import must_equal
from src.misc._internal_exceptions.comparison_exceptions import (
    BoolMismatchError, DictionaryKeysMismatchError, DictionaryMismatchError,
    DictionarySizeMismatchError, FloatMismatchError, IntegerMismatchError,
    ListMismatchError, ListSizeMismatchError, SetMismatchError,
    SetSizeMismatchError, TupleMismatchError, TupleSizeMismatchError,
    TypeMismatchError)
from src.test_utils import Test

# TODO test case where it wont crash and see context 


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

    with WillRaise(IntegerMismatchError) as context: 
        must_equal(a, b)

    must_equal('10 != 20', str(context.exception))


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

    with WillRaise(FloatMismatchError) as context:  
        must_equal(a, b)

    print(str(context.exception))
    must_equal('3.14 != 2.71', str(context.exception))



@Test.case
def test_float_precision() -> None:
    a = 0.1 + 0.2
    b = 0.3

    with WillRaise(FloatMismatchError) as context: 
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

    with WillRaise(BoolMismatchError) as context: 
        must_equal(a, b)

    print(str(context.exception))
    must_equal('True != False', str(context.exception))


#####################
### TUPLES
#####################


@Test.case
def test_tuple_match() -> None:
    a = (1, 2, 3)
    b = (1, 2, 3)

    must_equal(a, b)



@Test.case
def test_tuple_size_dont_match() -> None:
    a = (1, 2, 3)
    b = (1, 2, 3, 9)

    with WillRaise(TupleSizeMismatchError) as context: 
        must_equal(a, b)

    print(str(context.exception))
    must_equal('3 != 4 | tuple size mismatch', str(context.exception))



@Test.case
def test_tuple_dont_match() -> None:
    a = (1, 2, 3)
    b = (1, 2, 9)

    with WillRaise(TupleMismatchError) as context: 
        must_equal(a, b)

    print(str(context.exception))
    must_equal('(1, 2, 3) != (1, 2, 9) | element mismatch at index 2: 3 != 9', str(context.exception))


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

    with WillRaise(ListSizeMismatchError) as context: 
        must_equal(a, b)

    print(str(context.exception))
    must_equal('3 != 2 | length mismatch', str(context.exception))



@Test.case
def test_list_value_dont_match() -> None:
    a = [1, 2, 3]
    b = [1, 2, 4]

    with WillRaise(ListMismatchError) as context: 
        must_equal(a, b)

    print(str(context.exception))
    must_equal('[1, 2, 3] != [1, 2, 4] | element mismatch at index 2: 3 != 4', str(context.exception))



@Test.case
def test_nested_list_mismatch() -> None:
    a = [1, [2, 3], 4]
    b = [1, [2, 99], 4]

    with WillRaise(ListMismatchError) as context: 
        must_equal(a, b)

    print(str(context.exception))
    must_equal('[1, [2, 3], 4] != [1, [2, 99], 4] | element mismatch at index 1: [2, 3] != [2, 99]', str(context.exception))


#####################
### SETS
#####################


@Test.case
def test_set_match() -> None:
    a = {1, 2, 3}
    b = {1, 2, 3}

    must_equal(a, b)



@Test.case
def test_set_size_dont_match() -> None:
    a = {1, 2, 3}
    b = {1, 2, 3, 6}

    with WillRaise(SetSizeMismatchError) as context: 
        must_equal(a, b)

    print(str(context.exception))
    must_equal('3 != 4 | set size mismatch', str(context.exception))



@Test.case
def test_set_dont_match() -> None:
    a = {1, 2, 3}
    b = {1, 2, 4}

    with WillRaise(SetMismatchError) as context: 
        must_equal(a, b)

    print(str(context.exception))
    must_equal('{1, 2, 3} != {1, 2, 4} | missing={3} extra={4}', str(context.exception))


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
def test_dict_size_mismatch() -> None:
    a = {"x": 1, "y": 2, "z": 1}
    b = {"x": 1, "y": 2}

    with WillRaise(DictionarySizeMismatchError) as context: 
        must_equal(a, b)

    print(str(context.exception))
    must_equal('3 != 2 | size mismatch', str(context.exception))



@Test.case
def test_dict_key_mismatch() -> None:
    a = {"x": 1, "y": 2}
    b = {"x": 1, "z": 2}

    with WillRaise(DictionaryKeysMismatchError) as context: 
        must_equal(a, b)

    print(str(context.exception))
    must_equal("['x', 'y'] != ['x', 'z'] | key mismatch", str(context.exception))



@Test.case
def test_dict_value_mismatch() -> None:
    a = {"x": 1, "y": 2}
    b = {"x": 1, "y": 3}

    with WillRaise(DictionaryMismatchError) as context: 
        must_equal(a, b)

    print(str(context.exception))
    must_equal("{'x': 1, 'y': 2} != {'x': 1, 'y': 3} | value mismatch at key y: 2 != 3", str(context.exception))



@Test.case
def test_nested_dict() -> None:
    a = {"a": {"b": {"c": 1}}}
    b = {"a": {"b": {"c": 2}}}

    with WillRaise(DictionaryMismatchError) as context: 
        must_equal(a, b)

    print(str(context.exception))
    must_equal("{'a': {'b': {'c': 1}}} != {'a': {'b': {'c': 2}}} | value mismatch at key a: {'b': {'c': 1}} != {'b': {'c': 2}}", str(context.exception))



#####################
### MISC
#####################


@Test.case
def test_type_mismatch_int_str() -> None:
    a = 10
    b = "10"

    with WillRaise(TypeMismatchError) as context: 
        must_equal(a, b)

    print(str(context.exception))
    must_equal('Expected type <int> is different from <str>', str(context.exception))



@Test.case
def test_none_vs_int() -> None:

    with WillRaise(TypeMismatchError) as context: 
        must_equal(None, 1)

    print(str(context.exception))
    must_equal('Expected type <NoneType> is different from <int>', str(context.exception))



@Test.case
def test_none_vs_none() -> None:

    must_equal(None, None)

