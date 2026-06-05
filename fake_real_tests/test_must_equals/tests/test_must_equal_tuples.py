from tini_test.context_managers import WillRaise
from tini_test.misc.exceptions import ExpectedWasDifferentFromActual
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test


@Test.case
def test_tuple_equal_simple() -> None:
    expected = (1, 2, 3)
    actual = (1, 2, 3)
    must_equal(expected, actual)


@Test.case
def test_tuple_value_diff() -> None:
    expected = (1, 2, 3)
    actual = (1, 9, 3)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_tuple_length_diff() -> None:
    expected = (1, 2, 3)
    actual = (1, 2)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_tuple_empty() -> None:
    expected = ()
    actual = ()
    must_equal(expected, actual)


@Test.case
def test_tuple_nested_equal() -> None:
    expected = (1, (2, 3))
    actual = (1, (2, 3))
    must_equal(expected, actual)


@Test.case
def test_tuple_nested_diff() -> None:
    expected = (1, (2, 3))
    actual = (1, (2, 9))

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_tuple_mixed() -> None:
    expected = (1, 'a', 3.0)
    actual = (1, 'a', 3.0)
    must_equal(expected, actual)


@Test.case
def test_tuple_mixed_fail() -> None:
    expected = (1, 'a', 3.0)
    actual = (1, 'b', 3.0)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_tuple_single() -> None:
    expected = (1,)
    actual = (1,)
    must_equal(expected, actual)


@Test.case
def test_tuple_single_fail() -> None:
    expected = (1,)
    actual = (2,)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')