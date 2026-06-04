from tiny_test.context_manager import WillRaise
from tiny_test.misc.exceptions import ExpectedWasDifferentFromActual
from tiny_test.must_equals import must_equal
from tiny_test.test_utils import Test


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

    must_equal('''
ITEM: set mismatch
missing: {3}
extra: set()
''', str(context.exception))
    


@Test.case
def test_set_extra() -> None:
    expected = {1, 2}
    actual = {1, 2, 3}

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal('''
ITEM: set mismatch
missing: set()
extra: {3}
''', str(context.exception))
    


@Test.case
def test_set_value_diff() -> None:
    expected = {1, 2, 3}
    actual = {1, 9, 3}

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal('''
ITEM: set mismatch
missing: {2}
extra: {9}
''', str(context.exception))
    


@Test.case
def test_set_empty() -> None:
    expected: set = set()
    actual: set = set()
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

    must_equal('''
ITEM: set mismatch
missing: {1}
extra: {2}
''', str(context.exception))



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

    must_equal('''
ITEM: set mismatch
missing: {49}
extra: set()
''', str(context.exception))



@Test.case
def test_set_strings() -> None:
    expected = {'a', 'b', 'c'}
    actual = {'a', 'b', 'c'}
    must_equal(expected, actual)
