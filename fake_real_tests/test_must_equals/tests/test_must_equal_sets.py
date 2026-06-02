from src.context_manager import WillRaise
from src.misc.exceptions import ExpectedWasDifferentFromActual
from src.must_equals import must_equal
from src.test_utils import Test


@Test.case
def test_set_equal() -> None:
    expected = {1, 2, 3}
    actual = {1, 2, 3}
    must_equal(expected, actual)


@Test.case
def test_set_missing() -> None:
    expected = {1, 2, 3}
    actual = {1, 2}

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_set_extra() -> None:
    expected = {1, 2}
    actual = {1, 2, 3}

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_set_value_diff() -> None:
    expected = {1, 2, 3}
    actual = {1, 9, 3}

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_set_empty() -> None:
    expected = set()
    actual = set()
    must_equal(expected, actual)


@Test.case
def test_set_single() -> None:
    expected = {1}
    actual = {1}
    must_equal(expected, actual)


@Test.case
def test_set_single_fail() -> None:
    expected = {1}
    actual = {2}

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_set_large() -> None:
    expected = set(range(50))
    actual = set(range(50))
    must_equal(expected, actual)


@Test.case
def test_set_large_fail() -> None:
    expected = set(range(50))
    actual = set(range(49))  # missing last

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal(expected, actual)


@Test.case
def test_set_strings() -> None:
    expected = {"a", "b", "c"}
    actual = {"a", "b", "c"}
    must_equal(expected, actual)