from src.context_manager import WillRaise
from src.misc.exceptions import ExpectedWasDifferentFromActual
from src.must_equals import must_equal
from src.test_utils import Test


@Test.case
def test_list_equal_simple() -> None:
    expected = [1, 2, 3]
    actual = [1, 2, 3]
    must_equal(expected, actual)


@Test.case
def test_list_value_diff() -> None:
    expected = [1, 2, 3]
    actual = [1, 9, 3]

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_list_length_diff_shorter() -> None:
    expected = [1, 2, 3]
    actual = [1, 2]

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_list_length_diff_longer() -> None:
    expected = [1, 2]
    actual = [1, 2, 3]

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_list_empty() -> None:
    expected: list = []
    actual: list = []
    must_equal(expected, actual)


@Test.case
def test_list_nested_equal() -> None:
    expected = [1, [2, 3]]
    actual = [1, [2, 3]]
    must_equal(expected, actual)


@Test.case
def test_list_nested_diff() -> None:
    expected = [1, [2, 3]]
    actual = [1, [2, 9]]

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_list_mixed_types() -> None:
    expected = [1, 'a', 3.0]
    actual = [1, 'a', 3.0]
    must_equal(expected, actual)


@Test.case
def test_list_mixed_types_fail() -> None:
    expected = [1, 'a', 3.0]
    actual = [1, 'b', 3.0]

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_list_deep_nested() -> None:
    expected = [1, [2, [3, 4]]]
    actual = [1, [2, [3, 4]]]
    must_equal(expected, actual)