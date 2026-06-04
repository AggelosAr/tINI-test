import json

from tiny_test.context_manager import WillRaise
from tiny_test.misc.exceptions import ExpectedWasDifferentFromActual
from tiny_test.must_equals import must_equal
from tiny_test.test_utils import Test


@Test.case
def test_json_equal() -> None:
    expected = json.loads('{"a":1,"b":2}')
    actual = json.loads('{"a":1,"b":2}')
    must_equal(expected, actual)



@Test.case
def test_json_value_diff() -> None:
    expected = json.loads('{"a":1,"b":2}')
    actual = json.loads('{"a":1,"b":3}')

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_json_missing_key() -> None:
    expected = json.loads('{"a":1,"b":2}')
    actual = json.loads('{"a":1}')

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_json_extra_key() -> None:
    expected = json.loads('{"a":1}')
    actual = json.loads('{"a":1,"b":2}')

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_json_empty_object() -> None:
    expected = json.loads('{}')
    actual = json.loads('{}')
    must_equal(expected, actual)



@Test.case
def test_json_nested_equal() -> None:
    expected = json.loads('{"a":{"b":2}}')
    actual = json.loads('{"a":{"b":2}}')
    must_equal(expected, actual)



@Test.case
def test_json_nested_diff() -> None:
    expected = json.loads('{"a":{"b":2}}')
    actual = json.loads('{"a":{"b":9}}')

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_json_array_equal() -> None:
    expected = json.loads('{"a":[1,2,3]}')
    actual = json.loads('{"a":[1,2,3]}')
    must_equal(expected, actual)



@Test.case
def test_json_array_diff() -> None:
    expected = json.loads('{"a":[1,2,3]}')
    actual = json.loads('{"a":[1,9,3]}')

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_json_deep_equal() -> None:
    expected = json.loads('{"a":{"b":{"c":1}}}')
    actual = json.loads('{"a":{"b":{"c":1}}}')
    must_equal(expected, actual)



@Test.case
def test_json_deep_diff() -> None:
    expected = json.loads('{"a":{"b":{"c":1}}}')
    actual = json.loads('{"a":{"b":{"c":99}}}')

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_json_complex_structure_equal() -> None:
    expected = json.loads(
        '{"users":[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]}'
    )
    actual = json.loads(
        '{"users":[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]}'
    )

    must_equal(expected, actual)



@Test.case
def test_json_complex_structure_diff() -> None:
    expected = json.loads(
        '{"users":[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]}'
    )
    actual = json.loads(
        '{"users":[{"id":1,"name":"Alice"},{"id":2,"name":"Charlie"}]}'
    )

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')
