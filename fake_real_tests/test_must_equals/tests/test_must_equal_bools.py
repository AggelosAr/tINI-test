from small_test.context_manager import WillRaise
from small_test.misc.exceptions import ExpectedWasDifferentFromActual
from small_test.must_equals import must_equal
from small_test.test_utils import Test


@Test.case
def test_bool_true_true() -> None:
    expected = True
    actual = True
    must_equal(expected, actual)
    1/0



@Test.case
def test_bool_false_false() -> None:
    expected = False
    actual = False
    must_equal(expected, actual)
    1/0



@Test.case
def test_bool_true_false_fail() -> None:
    expected = True
    actual = False
    1/0

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal('''
True != False
''', str(context.exception))



@Test.case
def test_bool_false_true_fail() -> None:
    expected = False
    actual = True
    1/0

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal('''
False != True
''', str(context.exception))


@Test.case
def test_bool_identity_true() -> None:
    expected = bool(1)
    actual = True
    must_equal(expected, actual)


@Test.case
def test_bool_identity_false() -> None:
    expected = bool(0)
    actual = False
    must_equal(expected, actual)


@Test.case
def test_bool_truthy_int_fail() -> None:
    expected = True
    actual = 1

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal('''
ITEM: type mismatch
expected: <class 'bool'>
actual:   <class 'int'>
''', str(context.exception))



@Test.case
def test_bool_false_vs_zero_fail() -> None:
    expected = False
    actual = 0

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal('''
ITEM: type mismatch
expected: <class 'bool'>
actual:   <class 'int'>
''', str(context.exception))
    
