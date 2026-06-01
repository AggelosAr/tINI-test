from src.context_manager import WillRaise
from src.misc.exceptions import ExpectedWasDifferentFromActual
from src.must_equals import must_equal
from src.test_utils import Test



@Test.case
def test_must_equal_receives_more_args_than_expected() -> None:
    expected = (1, 2)
    actual = (1, 2, 3)

    with WillRaise(TypeError) as context:
        must_equal(expected, actual, 1)

    must_equal('must_equal() takes 2 positional arguments but 3 were given', str(context.exception))


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