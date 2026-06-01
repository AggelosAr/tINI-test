from src.context_manager import WillRaise
from src.misc.exceptions import (ComperatorIsNotValid,
                                 ComperatorWasNotProvided,
                                 ExpectedWasDifferentFromActual)
from src.must_equals import must_equal
from src.test_utils import Test


@Test.case
def test_must_equal_receives_not_a_valid_comperator() -> None:
    expected = (1, 2)
    actual = (1, 2, 3)

    with WillRaise(ComperatorIsNotValid) as context:
        must_equal(expected, actual, 1)

    must_equal('Comperator is not a function', str(context.exception))



@Test.case
def test_must_equal_receives_more_args_than_expected() -> None:
    expected = (1, 2)
    actual = (1, 2, 3)

    with WillRaise(TypeError) as context:
        must_equal(expected, actual, 1, 2)

    must_equal('must_equal() takes from 2 to 3 positional arguments but 4 were given', str(context.exception))



@Test.case
def test_must_equal_receives_unknwon_object_no_comperator_provided() -> None:

    class A:
        def __init__(self, a: int) -> None:
            self.a = 10

    with WillRaise(ComperatorWasNotProvided) as context:
        must_equal(A(10), A(20))

    must_equal('Unknown type encountered and a comperator was not provided.', str(context.exception))



@Test.case
def test_must_equal_frozen_set_passes() -> None:

    s = frozenset({1, 2, 3})
    t = frozenset({1, 2, 3})

    must_equal(s, t)



@Test.case
def test_must_equal_type_none() -> None:

    s = type(None)
    t = type(None)
    
    must_equal(s, t)



@Test.case
def test_tuple_size_dont_match() -> None:
    expected = (1, 2)
    actual = (1, 2, 3)

    must_equal(expected, actual)


@Test.case
def test_tuple_value_dont_match() -> None:
    expected = (1, 2, 3)
    actual = (1, 4, 3)

    must_equal(expected, actual)


@Test.case
def test_list_size_dont_match() -> None:
    expected = [1, 2]
    actual = [1, 2, 3]

    must_equal(expected, actual)


@Test.case
def test_list_value_dont_match() -> None:
    expected = [1, 2, 3]
    actual = [1, 4, 3]

    must_equal(expected, actual)


@Test.case
def test_multiline_string_diff() -> None:
    expected = 'hello\nworld\nfoo'
    actual = 'hello\nthere\nfoo'

    must_equal(expected, actual)



@Test.case
def test_dict_value_dont_match() -> None:
    expected = {'a': 1, 'b': 2}
    actual = {'a': 1, 'b': 3}
    
    must_equal(expected, actual)


@Test.case
def test_dict_value_dont_match_case() -> None:
    expected = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    actual = 'RRRRRRRRRRRRRRRRRRRRRRRsadasdasdasd'

    must_equal(expected, actual)


@Test.case
def test_equal_tuple_passes() -> None:
    expected = (1, 2, 3)
    actual = (1, 2, 3)

    must_equal(expected, actual)


@Test.case
def test_equal_multiline_string_passes() -> None:
    expected = 'a\nb\nc'
    actual = 'a\nb\nc'

    must_equal(expected, actual)


@Test.case
def test_ints_dont_match() -> None:
    expected = 10
    actual = 20

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    must_equal('10 != 20', str(context.exception))