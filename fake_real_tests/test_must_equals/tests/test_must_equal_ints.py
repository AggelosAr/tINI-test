from src.context_manager import WillRaise
from src.misc.exceptions import ExpectedWasDifferentFromActual
from src.must_equals import must_equal
from src.test_utils import Test

# TODO add tests for big numbers!


@Test.case
def test_int_equal_small() -> None:
    expected = 1
    actual = 1
    must_equal(expected, actual)



@Test.case
def test_int_equal_zero() -> None:
    expected = 0
    actual = 0
    must_equal(expected, actual)



@Test.case
def test_int_equal_negative() -> None:
    expected = -10
    actual = -10
    must_equal(expected, actual)



@Test.case
def test_int_mismatch_small() -> None:
    expected = 1
    actual = 2

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_int_mismatch_negative() -> None:
    expected = -1
    actual = 1

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_int_large_equal() -> None:
    expected = 10**12
    actual = 10**12
    must_equal(expected, actual)



@Test.case
def test_int_large_mismatch() -> None:
    expected = 10**12
    actual = 10**12 + 1

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_int_boundary_zero_positive() -> None:
    expected = 0
    actual = 1

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_int_boundary_zero_negative() -> None:
    expected = 0
    actual = -1

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_int_same_reference_values() -> None:
    expected = 42
    actual = 42
    must_equal(expected, actual)
