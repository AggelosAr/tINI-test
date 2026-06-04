from tiny_test.context_manager import WillRaise
from tiny_test.misc.exceptions import ExpectedWasDifferentFromActual
from tiny_test.must_equals import must_equal
from tiny_test.test_utils import Test


@Test.case
def test_dict_equal() -> None:
    expected = {'a': 1, 'b': 2}
    actual = {'a': 1, 'b': 2}
    must_equal(expected, actual)


@Test.case
def test_dict_value_diff() -> None:
    expected = {'a': 1, 'b': 2}
    actual = {'a': 1, 'b': 3}

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_dict_missing_key() -> None:
    expected = {'a': 1, 'b': 2}
    actual = {'a': 1}

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_dict_extra_key() -> None:
    expected = {'a': 1}
    actual = {'a': 1, 'b': 2}

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_dict_empty() -> None:
    expected: dict = {}
    actual: dict = {}
    must_equal(expected, actual)


@Test.case
def test_dict_nested_equal() -> None:
    expected = {'a': {'b': 2}}
    actual = {'a': {'b': 2}}
    must_equal(expected, actual)


@Test.case
def test_dict_nested_diff() -> None:
    expected = {'a': {'b': 2}}
    actual = {'a': {'b': 9}}

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_dict_mixed_values() -> None:
    expected = {'a': [1, 2]}
    actual = {'a': [1, 2]}
    must_equal(expected, actual)


@Test.case
def test_dict_mixed_values_fail() -> None:
    expected = {'a': [1, 2]}
    actual = {'a': [1, 9]}

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')


@Test.case
def test_dict_deep() -> None:
    expected = {'a': {'b': {'c': 1}}}
    actual = {'a': {'b': {'c': 1}}}
    must_equal(expected, actual)