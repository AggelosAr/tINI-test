from tini_test.context_manager import WillRaise
from tini_test.misc.exceptions import ExpectedWasDifferentFromActual
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test


@Test.case
def test_multiline_string_diff() -> None:
    expected = 'hello\nworld\nfoo'
    actual = 'hello\nthere\nfoo'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')
    
    must_equal('''
ITEM:
--- expected
+++ actual
@@ -1,3 +1,3 @@
 hello
-world
+there
 foo
''', str(context.exception))



@Test.case
def test_string_middle_character_different() -> None:
    expected = 'hello world'
    actual = 'hello there'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal('''
ITEM:
string mismatch at index 6
expected char: 'w'
actual char:   't'

expected: 'hello world'
actual:   'hello there'
                 ^
''', str(context.exception))
    


@Test.case
def test_string_last_character_different() -> None:
    expected = 'abcdef'
    actual = 'abcdeg'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal('''
ITEM:
string mismatch at index 5
expected char: 'f'
actual char:   'g'

expected: 'abcdef'
actual:   'abcdeg'
                ^
''', str(context.exception))
    


@Test.case
def test_string_actual_shorter() -> None:
    expected = 'abcdef'
    actual = 'abc'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal('''
ITEM:
string mismatch at index 3
expected char: 'd'
actual char:   <end-of-string>

expected: 'abcdef'
actual:   'abc'
              ^
''', str(context.exception))
    


@Test.case
def test_string_actual_longer() -> None:
    expected = 'abc'
    actual = 'abcdef'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal('''
ITEM:
string mismatch at index 3
expected char: <end-of-string>
actual char:   'd'

expected: 'abc'
actual:   'abcdef'
              ^
''', str(context.exception))
    


@Test.case
def test_multiline_string_diff_case() -> None:
    expected = (
        'hello\n'
        'world\n'
        'foo'
    )

    actual = (
        'hello\n'
        'there\n'
        'foo'
    )

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal('''
ITEM:
--- expected
+++ actual
@@ -1,3 +1,3 @@
 hello
-world
+there
 foo
''', str(context.exception))
    


@Test.case
def test_multiline_string_diff_case_special() -> None:
    expected = (
        'hello Again my little garden\n'
        'world was a small bee nest\n'
        'in the other side'
    )

    actual = (
        'hello Again my little garden\n'
        'world was a XXX bee next\n'
        'in the other side'
    )

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal('''
ITEM:
--- expected
+++ actual
@@ -1,3 +1,3 @@
 hello Again my little garden
-world was a small bee nest
+world was a XXX bee next
 in the other side
''', str(context.exception))



@Test.case
def test_dict_value_dont_match_case() -> None:
    expected = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    actual = 'RRRRRRRRRRRRRRRRRRRRRRRsadasdasdasd'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    must_equal('''
ITEM:
string mismatch at index 0
expected char: 'X'
actual char:   'R'

expected: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
actual:   'RRRRRRRRRRRRRRRRRRRRRRRsadasda'
           ^
''', str(context.exception))



@Test.case
def test_str_empty() -> None:
    expected = ''
    actual = ''
    must_equal(expected, actual)



@Test.case
def test_str_unicode() -> None:
    expected = '🔥'
    actual = '🔥'
    must_equal(expected, actual)



@Test.case
def test_str_unicode_fail() -> None:
    expected = '🔥a'
    actual = '🔥b'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_str_long_equal() -> None:
    expected = 'a' * 100
    actual = 'a' * 100
    must_equal(expected, actual)



@Test.case
def test_str_long_fail() -> None:
    expected = 'a' * 100
    actual = 'a' * 99 + 'b'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')



@Test.case
def test_str_very_long() -> None:
    expected = 'a' * 2**16 + 'X'
    actual = 'a' * 2**16 + 'b'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('---------------------------------')
    print(str(context.exception))
    print('---------------------------------')

    must_equal('''
String mismatch
''', str(context.exception))
  