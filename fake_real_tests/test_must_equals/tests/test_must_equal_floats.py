from src.context_manager import WillRaise
from src.misc.exceptions import ExpectedWasDifferentFromActual
from src.must_equals import must_equal
from src.test_utils import Test


@Test.case
def test_float_equal_simple() -> None:
    expected = 1.0
    actual = 1.0
    must_equal(expected, actual)


@Test.case
def test_float_mismatch() -> None:
    expected = 1.0
    actual = 2.0

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_float_precision_equal() -> None:
    expected = 0.1 + 0.2
    actual = 0.3
    must_equal(expected, actual)


@Test.case
def test_float_precision_mismatch() -> None:
    expected = 0.1
    actual = 0.2

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_float_negative() -> None:
    expected = -1.5
    actual = -1.5
    must_equal(expected, actual)


@Test.case
def test_float_zero() -> None:
    expected = 0.0
    actual = 0.0
    must_equal(expected, actual)


@Test.case
def test_float_large() -> None:
    expected = 1e9
    actual = 1e9
    must_equal(expected, actual)


@Test.case
def test_float_small_diff_fail() -> None:
    expected = 1.0000001
    actual = 1.0000002

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_float_nan_case() -> None:
    expected = float("nan")
    actual = float("nan")

    # NaN != NaN so this is expected failure behavior
    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_float_infinity() -> None:
    expected = float("inf")
    actual = float("inf")
    must_equal(expected, actual)
