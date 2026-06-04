from small_test.context_manager import WillRaise
from small_test.misc.exceptions import ExpectedWasDifferentFromActual
from small_test.must_equals import must_equal
from small_test.test_utils import Test


@Test.case
def test_bytes_equal() -> None:
    expected = b'hello'
    actual = b'hello'
    must_equal(expected, actual)



@Test.case
def test_bytes_diff_content() -> None:
    expected = b'hello'
    actual = b'world'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_bytes_empty() -> None:
    expected = b''
    actual = b''
    must_equal(expected, actual)



@Test.case
def test_bytes_empty_vs_non_empty() -> None:
    expected = b''
    actual = b'a'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_bytes_single_byte_equal() -> None:
    expected = b'\x00'
    actual = b'\x00'
    must_equal(expected, actual)



@Test.case
def test_bytes_single_byte_diff() -> None:
    expected = b'\x00'
    actual = b'\x01'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_bytes_binary_data_equal() -> None:
    expected = bytes([0, 1, 2, 3, 255])
    actual = bytes([0, 1, 2, 3, 255])
    must_equal(expected, actual)



@Test.case
def test_bytes_binary_data_diff() -> None:
    expected = bytes([0, 1, 2, 3, 255])
    actual = bytes([0, 1, 2, 4, 255])

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_bytes_long_equal() -> None:
    expected = b'a' * 1000
    actual = b'a' * 1000
    must_equal(expected, actual)



@Test.case
def test_bytes_long_diff_end() -> None:
    expected = b'a' * 999 + b'b'
    actual = b'a' * 1000

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_bytes_utf8_equal() -> None:
    expected = 'hello world'.encode('utf-8')
    actual = 'hello world'.encode('utf-8')
    must_equal(expected, actual)



@Test.case
def test_bytes_utf8_diff() -> None:
    expected = 'hello world'.encode('utf-8')
    actual = 'hello there'.encode('utf-8')

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')
