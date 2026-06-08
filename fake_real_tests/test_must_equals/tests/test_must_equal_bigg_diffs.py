import json
import os

from tini_test.context_managers import WillRaise
from tini_test.misc.exceptions import ExpectedWasDifferentFromActual
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test


@Test.case
def test_big_json_no_diff() -> None:
    
    root_path = '/home/papaggalos/workspace/python_projects/tINI-test/fake_real_tests/test_must_equals/tests'
    
    with open(os.path.join(root_path, 'json_expected.json')) as f:
        expected = json.load(f)

    with open(os.path.join(root_path, 'json_actual.json')) as f:
        actual = json.load(f)

    must_equal(expected, actual)



@Test.case
def test_big_json_diff() -> None:
    
    root_path = '/home/papaggalos/workspace/python_projects/tINI-test/fake_real_tests/test_must_equals/tests'
    
    with open(os.path.join(root_path, 'json_expected.json')) as f:
        expected = json.load(f)

    with open(os.path.join(root_path, 'json_actual_broken.json')) as f:
        actual = json.load(f)
    

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)


    must_equal(r'''
ITEM[4]['about']:
--- expected
+++ actual

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -1 +1 @@

~~~~~~~~~~~~~~~~~~~~~~~~

string mismatch at index 1511
expected char: 'p'
actual char:   'D'

expected: 'oris. Consectetur aliqua consequat proident qui.\r\n'
actual:   'oris. Consectetur aliqua consequat DIFFERENCE qui.\r\n'
                                              ^

[EOD]''', str(context.exception))



@Test.case
def test_big_single_line_string_diff() -> None:
    
    expected = 'Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint. Consectetur fugiat nostrud excepteur id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad. Duis aliqua et labore ea. Ad qui magna consectetur amet enim consequat ullamco ea pariatur reprehenderit consectetur dolore est laboris. Consectetur aliqua consequat proident qui'
    actual = 'Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint. Consectetur fugiat nostrud excepteur id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad. Duis aliqua et labore ea. Ad qui magna consectetur amet enim consequat ullamco ea pariatur reprehenderit consectetur dolore est laboris. Consectetur aliqua consequat proident DIFFERENCE'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    must_equal('''
ITEM:
string mismatch at index 880
expected char: 'q'
actual char:   'D'

expected: 'sectetur aliqua consequat proident qui'
actual:   'sectetur aliqua consequat proident DIFFERENCE'
                                              ^
[EOD]''', str(context.exception))
    


@Test.case
def test_big_multi_line_string_diff() -> None:
    
    expected = 'Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint. Consectetur fugiat nostrud excepteur id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad. Duis aliqua et labore ea. Ad qui magna consectetur amet enim consequat ullamco ea pariatur reprehenderit consectetur dolore est laboris. Consectetur aliqua consequat proident qui'
    actual = 'Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint. Consectetur fugiat nostrud excepteur id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad. Duis aliqua et labore ea. Ad qui magna consectetur amet enim consequat ullamco ea pariatur reprehenderit consectetur dolore est laboris. Consectetur aliqua consequat proident DIFFERENCE'

    expected = expected.replace('.', '\n')
    actual = actual.replace('.', '\n')

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    must_equal('''
ITEM:
--- expected
+++ actual

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -16,4 +16,4 @@

~~~~~~~~~~~~~~~~~~~~~~~~
  Consectetur fugiat nostrud except[TRUNCATED<35>chars]i laborum eu ut commodo laboris ad
  Duis aliqua et labore ea
  Ad qui magna consectetur amet eni[TRUNCATED<42>chars]rit consectetur dolore est laboris

string mismatch at index 39
expected char: 'q'
actual char:   'D'

expected: 'sectetur aliqua consequat proident qui'
actual:   'sectetur aliqua consequat proident DIFFERENCE'
                                              ^

[EOD]''', str(context.exception))



@Test.case
def test_big_multi_line_string_diff_case_and_omitted_diffs() -> None:
    
    expected = '''Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Consectetur fugiat nostrud excepteur id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad. id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad. id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.
    Duis aliqua et labore ea.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Ad qui magna consectetur amet enim consequat ullamco ea pariatur reprehenderit consectetur dolore est laboris. 
    Consectetur aliqua consequat proident qui'''

    actual = '''YYYOfficia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    OXficia in dolor excepteur ullamco sint.
    OYficia in dolor excepteur ullamco sint.
    OZficia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Consectetur fugiat nostrud DIFFFFFF id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad. id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad. id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad. 
    Duis aliqua et labore ea.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    XXXOfficia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    Officia in dolor excepteur ullamco sint.
    CCCAd qui magna consectetur amet enim consequat ullamco ea pariatur reprehenderit consectetur dolore est laboris. 
    Consectetur aliqua consequat proident qui'''
    
    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)
   
    
    must_equal(r'''
ITEM:
--- expected
+++ actual

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -1,4 +1,11 @@

~~~~~~~~~~~~~~~~~~~~~~~~

string mismatch at index 0
expected char: 'O'
actual char:   'Y'

expected: 'Officia in dolor excepteur ullamco '
actual:   'YYYOfficia in dolor excepteur ullam'
           ^
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -26,14 +33,7 @@

~~~~~~~~~~~~~~~~~~~~~~~~
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

string mismatch at index 5
expected char: 'f'
actual char:   'X'

expected: '    Officia in dolor excepteur ullamco s'
actual:   '    OXficia in dolor excepteur ullamco s'
                ^

string mismatch at index 5
expected char: 'f'
actual char:   'Y'

expected: '    Officia in dolor excepteur ullamco s'
actual:   '    OYficia in dolor excepteur ullamco s'
                ^

string mismatch at index 5
expected char: 'f'
actual char:   'Z'

expected: '    Officia in dolor excepteur ullamco s'
actual:   '    OZficia in dolor excepteur ullamco s'
                ^

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -62,7 +62,7 @@

~~~~~~~~~~~~~~~~~~~~~~~~
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

string mismatch at index 4
expected char: 'O'
actual char:   'X'

expected: '    Officia in dolor excepteur ullamco '
actual:   '    XXXOfficia in dolor excepteur ullam'
               ^
     Officia in dolor excepteur ull[TRUNCATED<376>chars]a in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

... additional differences omitted (1+ more) ...

[EOD]''', str(context.exception))
    


@Test.case
def test_single_line_diff_weird_case() -> None:

    actual = 'ea pariatur reprehenderit consectetur dolore est laboris. Consectetur aliqua consequat proident qui.\r\n'
    expected = 'ea pariatur reprehenderit consectetur dolore est laboris. Consectetur aliqua consequat proident qui.\r\n'

    must_equal(actual, expected)



@Test.case
def xxxyyyzzz() -> None:

    must_equal(r'''
ITEM:
--- expected
+++ actual

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -1,4 +1,11 @@

~~~~~~~~~~~~~~~~~~~~~~~~

string mismatch at index 0
expected char: 'O'
actual char:   'Y'

expected: 'Officia in dolor excepteur ullamco sint.\\n\\n'
actual:   'YYYOfficia in dolor excepteur ullamco sint.\\n'
           ^

     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -26,14 +33,7 @@

~~~~~~~~~~~~~~~~~~~~~~~~
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

string mismatch at index 5
expected char: 'f'
actual char:   'X'

expected: '    Officia in dolor excepteur ullamco sint.\n'
actual:   '    OXficia in dolor excepteur ullamco sint.\n'
                ^

string mismatch at index 5
expected char: 'f'
actual char:   'Y'

expected: '    Officia in dolor excepteur ullamco sint.\n'
actual:   '    OYficia in dolor excepteur ullamco sint.\n'
                ^

string mismatch at index 5
expected char: 'f'
actual char:   'Z'

expected: '    Officia in dolor excepteur ullamco sint.\n'
actual:   '    OZficia in dolor excepteur ullamco sint.\n'
                ^

string mismatch at index 31
expected char: 'e'
actual char:   'D'

expected: '    Consectetur fugiat nostrud excepteur id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deser'
actual:   '    Consectetur fugiat nostrud DIFFFFFF id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deseru'
                                          ^
     Duis aliqua et labore ea.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -62,7 +62,7 @@

~~~~~~~~~~~~~~~~~~~~~~~~
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

string mismatch at index 4
expected char: 'O'
actual char:   'X'

expected: '    Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor exc'
actual:   '    XXXOfficia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor '
               ^
     Officia in dolor excepteur ullamco sint.Offic[TRUNCATED<346>chars]mco sint.Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

... additional differences omitted (1+ more) ...

''', r'''
ITEM:
--- expected
+++ actual

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -1,4 +1,11 @@

~~~~~~~~~~~~~~~~~~~~~~~~

string mismatch at index 0
expected char: 'O'
actual char:   'Y'

expected: 'Officia in dolor excepteur ullamco sint.\\n\\n'
actual:   'YYYOfficia in dolor excepteur ullamco sint.\\n'
           ^

     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -26,14 +33,7 @@

~~~~~~~~~~~~~~~~~~~~~~~~
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

string mismatch at index 5
expected char: 'f'
actual char:   'X'

expected: '    Officia in dolor excepteur ullamco sint.\n'
actual:   '    OXficia in dolor excepteur ullamco sint.\n'
                ^

string mismatch at index 5
expected char: 'f'
actual char:   'Y'

expected: '    Officia in dolor excepteur ullamco sint.\n'
actual:   '    OYficia in dolor excepteur ullamco sint.\n'
                ^

string mismatch at index 5
expected char: 'f'
actual char:   'Z'

expected: '    Officia in dolor excepteur ullamco sint.\n'
actual:   '    OZficia in dolor excepteur ullamco sint.\n'
                ^

string mismatch at index 31
expected char: 'e'
actual char:   'D'

expected: '    Consectetur fugiat nostrud excepteur id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deser'
actual:   '    Consectetur fugiat nostrud DIFFFFFF id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deseru'
                                          ^
     Duis aliqua et labore ea.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -62,7 +62,7 @@

~~~~~~~~~~~~~~~~~~~~~~~~
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

string mismatch at index 4
expected char: 'O'
actual char:   'X'

expected: '    Officia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor exc'
actual:   '    XXXOfficia in dolor excepteur ullamco sint.Officia in dolor excepteur ullamco sint.Officia in dolor '
               ^
     Officia in dolor excepteur ullamco sint.Offic[TRUNCATED<346>chars]mco sint.Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.

... additional differences omitted (1+ more) ...

''')


@Test.case
def heavy_nest():

    actual = {
        'metadata': {
            'version': 3,
            'created': '2026-06-08T12:34:56Z',
            'active': True,
            'tags': {'demo', 'nested', 'complex', 'python'},
            'checksum': None,
        },
        'users': [
            {
                'id': 1001,
                'name': 'Alice',
                'age': 31,
                'scores': [98, 87, 91],
                'preferences': {
                    'theme': 'dark',
                    'notifications': {
                        'email': True,
                        'sms': False,
                        'push': True,
                    },
                    'favorite_numbers': (3, 7, 11, 13),
                },
                'addresses': [
                    {
                        'type': 'home',
                        'location': {
                            'country': 'USA',
                            'city': 'Seattle',
                            'coordinates': (47.6062, -122.3321),
                        },
                    },
                    {
                        'type': 'work',
                        'location': {
                            'country': 'USA',
                            'city': 'Bellevue',
                            'coordinates': (47.6101, -122.2015),
                        },
                    },
                ],
            },
            {
                'id': 1002,
                'name': 'Bob',
                'age': 27,
                'scores': [76, 82, 89],
                'preferences': {
                    'theme': 'light',
                    'notifications': {
                        'email': False,
                        'sms': True,
                        'push': False,
                    },
                    'favorite_numbers': (2, 4, 8, 16),
                },
                'addresses': [],
            },
        ],
        'inventory': {
            'warehouse_a': {
                'items': [
                    {
                        'sku': 'A-001',
                        'name': 'Widget',
                        'price': 19.99,
                        'stock': 500,
                        'attributes': {
                            'colors': ['red', 'blue', 'green'],
                            'sizes': ['S', 'M', 'L'],
                            'dimensions': {
                                'width': 12.5,
                                'height': 8.0,
                                'depth': 4.2,
                            },
                        },
                    },
                    {
                        'sku': 'A-002',
                        'name': 'Gadget',
                        'price': 49.95,
                        'stock': 125,
                        'attributes': {
                            'colors': ['black'],
                            'sizes': [],
                            'dimensions': {
                                'width': 20.0,
                                'height': 5.0,
                                'depth': 2.5,
                            },
                        },
                    },
                ]
            },
            'warehouse_b': {
                'items': [],
                'capacity': 10000,
            },
        },
        'analytics': {
            'daily': [
                {'date': '2026-06-01', 'visits': 10234, 'conversion': 0.034},
                {'date': '2026-06-02', 'visits': 11287, 'conversion': 0.031},
                {'date': '2026-06-03', 'visits': 10891, 'conversion': 0.036},
            ],
            'aggregates': {
                'total_visits': 32412,
                'average_conversion': 0.0337,
                'histogram': {
                    '0-10': 12,
                    '10-20': 33,
                    '20-30': 25,
                    '30+': 8,
                },
            },
        },
        'configuration': {
            'services': {
                'database': {
                    'host': 'db.internal',
                    'port': 5432,
                    'replicas': [
                        {'host': 'db-replica-1.internal', 'port': 5432},
                        {'host': 'db-replica-2.internal', 'port': 5432},
                    ],
                },
                'cache': {
                    'host': 'cache.internal',
                    'port': 6379,
                    'enabled': True,
                },
            },
            'feature_flags': {
                'new_dashboard': True,
                'beta_search': False,
                'experimental': {
                    'group_a': {'enabled': True, 'rollout': 0.25},
                    'group_b': {'enabled': False, 'rollout': 0.0},
                },
            },
        },
        'graph': {
            'nodes': {
                'n1': {'label': 'Start'},
                'n2': {'label': 'Process'},
                'n3': {'label': 'End'},
            },
            'edges': [
                ('n1', 'n2'),
                ('n2', 'n3'),
            ],
        },
        'mixed_values': [
            None,
            True,
            False,
            123,
            45.67,
            'hello world',
            b'binary-data',
            [1, 2, {'a': [3, 4, {'b': 5}, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, {
                                                                                                                                                                                                                                                    'metadata': {
                                                                                                                                                                                                                                                        'version': 3,
                                                                                                                                                                                                                                                        'created': '2026-06-08T12:34:56Z',
                                                                                                                                                                                                                                                        'active': True,
                                                                                                                                                                                                                                                        'tags': {'demo', 'nested', 'complex', 'python', },
                                                                                                                                                                                                                                                        'checksum': None,
                                                                                                                                                                                                                                                        'NEST_1': {
                                                                                                                                                                                                                                                            'NEST_2': {
                                                                                                                                                                                                                                                                'NEST_3': {
                                                                                                                                                                                                                                                                    'NEST_4': {
                                                                                                                                                                                                                                                                        'NEST_5': {
                                                                                                                                                                                                                                                                            'NEST_6': {
                                                                                                                                                                                                                                                                                'NEST_7': {
                                                                                                                                                                                                                                                                                    'NEST_8': {
                                                                                                                                                                                                                                                                                        'NEST_9': {
                                                                                                                                                                                                                                                                                            'NEST_1': {
                                                                                                                                                                                                                                                                                                'NEST_2': {
                                                                                                                                                                                                                                                                                                    'NEST_3': {
                                                                                                                                                                                                                                                                                                        'NEST_4': {
                                                                                                                                                                                                                                                                                                            'NEST_5': {
                                                                                                                                                                                                                                                                                                                'NEST_6': {
                                                                                                                                                                                                                                                                                                                    'NEST_7': {
                                                                                                                                                                                                                                                                                                                        'NEST_8': {
                                                                                                                                                                                                                                                                                                                            'NEST_9': {
                                                                                                                                                                                                                                                                                                                                'NEST_1': {
                                                                                                                                                                                                                                                                                                                                    'NEST_2': {
                                                                                                                                                                                                                                                                                                                                        'NEST_3': {
                                                                                                                                                                                                                                                                                                                                            'NEST_4': {
                                                                                                                                                                                                                                                                                                                                                'NEST_5': {
                                                                                                                                                                                                                                                                                                                                                    'NEST_6': {
                                                                                                                                                                                                                                                                                                                                                        'NEST_7': {
                                                                                                                                                                                                                                                                                                                                                            'NEST_8': {
                                                                                                                                                                                                                                                                                                                                                                'NEST_9': {
                                                                                                                                                                                                                                                                                                                                                                    'EDGE': 'I AM THE EDGE'
                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                        }

                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                    'users': [
                                                                                                                                                                                                                                                        {
                                                                                                                                                                                                                                                            'fake_user': 'I could be free … If I could pluck out the memory of him from my heart as easily as his heart was plucked from the fire, I could be free. I discover that grief means living with someone who is no longer there. The Buddhists believe that our returning spirit may inhabit any form it chooses. Is that him? Mistletoe on the winter oak. Is that him? Swooping above me in the body of a bird. I could wear him on my finger in the ring he gave me. If I rub it, will he appear again in human form?',
                                                                                                                                                                                                                                                            'id': 1001,
                                                                                                                                                                                                                                                            'name': 'Alice',
                                                                                                                                                                                                                                                            'age': 31,
                                                                                                                                                                                                                                                            'scores': [98, 87, 91],
                                                                                                                                                                                                                                                            'preferences': {
                                                                                                                                                                                                                                                                'theme': 'dark',
                                                                                                                                                                                                                                                                'notifications': {
                                                                                                                                                                                                                                                                    'email': True,
                                                                                                                                                                                                                                                                    'sms': False,
                                                                                                                                                                                                                                                                    'push': True,
                                                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                                                'favorite_numbers': (3, 7, 11, 13),
                                                                                                                                                                                                                                                            },
                                                                                                                                                                                                                                                            'addresses': [
                                                                                                                                                                                                                                                                {
                                                                                                                                                                                                                                                                    'type': 'home',
                                                                                                                                                                                                                                                                    'location': {
                                                                                                                                                                                                                                                                        'country': 'USA',
                                                                                                                                                                                                                                                                        'city': 'Seattle',
                                                                                                                                                                                                                                                                        'coordinates': (47.6062, -122.3321),
                                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                                                {
                                                                                                                                                                                                                                                                    'type': 'work',
                                                                                                                                                                                                                                                                    'location': {
                                                                                                                                                                                                                                                                        'country': 'USA',
                                                                                                                                                                                                                                                                        'city': 'Bellevue',
                                                                                                                                                                                                                                                                        'coordinates': (47.6101, -122.2015),
                                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                                            ],
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                        {
                                                                                                                                                                                                                                                            'id': 1002,
                                                                                                                                                                                                                                                            'name': 'Bob',
                                                                                                                                                                                                                                                            'age': 27,
                                                                                                                                                                                                                                                            'scores': [76, 82, 89],
                                                                                                                                                                                                                                                            'preferences': {
                                                                                                                                                                                                                                                                'theme': 'light',
                                                                                                                                                                                                                                                                'notifications': {
                                                                                                                                                                                                                                                                    'email': False,
                                                                                                                                                                                                                                                                    'sms': True,
                                                                                                                                                                                                                                                                    'push': False,
                                                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                                                'favorite_numbers': (2, 4, 8, 16),
                                                                                                                                                                                                                                                            },
                                                                                                                                                                                                                                                            'addresses': [],
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                    ],
                                                                                                                                                                                                                                                    'inventory': {
                                                                                                                                                                                                                                                        'warehouse_a': {
                                                                                                                                                                                                                                                            'items': [
                                                                                                                                                                                                                                                                {
                                                                                                                                                                                                                                                                    'sku': 'A-001',
                                                                                                                                                                                                                                                                    'name': 'Widget',
                                                                                                                                                                                                                                                                    'price': 19.99,
                                                                                                                                                                                                                                                                    'stock': 500,
                                                                                                                                                                                                                                                                    'attributes': {
                                                                                                                                                                                                                                                                        'colors': ['red', 'blue', 'green'],
                                                                                                                                                                                                                                                                        'sizes': ['S', 'M', 'L'],
                                                                                                                                                                                                                                                                        'dimensions': {
                                                                                                                                                                                                                                                                            'width': 12.5,
                                                                                                                                                                                                                                                                            'height': 8.0,
                                                                                                                                                                                                                                                                            'depth': 4.2,
                                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                                                {
                                                                                                                                                                                                                                                                    'sku': 'A-002',
                                                                                                                                                                                                                                                                    'name': 'Gadget',
                                                                                                                                                                                                                                                                    'price': 49.95,
                                                                                                                                                                                                                                                                    'stock': 125,
                                                                                                                                                                                                                                                                    'attributes': {
                                                                                                                                                                                                                                                                        'colors': ['black'],
                                                                                                                                                                                                                                                                        'sizes': [],
                                                                                                                                                                                                                                                                        'dimensions': {
                                                                                                                                                                                                                                                                            'width': 20.0,
                                                                                                                                                                                                                                                                            'height': 5.0,
                                                                                                                                                                                                                                                                            'depth': 2.5,
                                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                                            ]
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                        'warehouse_b': {
                                                                                                                                                                                                                                                            'items': [],
                                                                                                                                                                                                                                                            'capacity': 10000,
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                    'analytics': {
                                                                                                                                                                                                                                                        'daily': [
                                                                                                                                                                                                                                                            {'date': '2026-06-01', 'visits': 10234, 'conversion': 0.034},
                                                                                                                                                                                                                                                            {'date': '2026-06-02', 'visits': 11287, 'conversion': 0.031},
                                                                                                                                                                                                                                                            {'date': '2026-06-03', 'visits': 10891, 'conversion': 0.036},
                                                                                                                                                                                                                                                        ],
                                                                                                                                                                                                                                                        'aggregates': {
                                                                                                                                                                                                                                                            'total_visits': 32412,
                                                                                                                                                                                                                                                            'average_conversion': 0.0337,
                                                                                                                                                                                                                                                            'histogram': {
                                                                                                                                                                                                                                                                '0-10': 12,
                                                                                                                                                                                                                                                                '10-20': 33,
                                                                                                                                                                                                                                                                '20-30': 25,
                                                                                                                                                                                                                                                                '30+': 8,
                                                                                                                                                                                                                                                            },
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                    'configuration': {
                                                                                                                                                                                                                                                        'services': {
                                                                                                                                                                                                                                                            'database': {
                                                                                                                                                                                                                                                                'host': 'db.internal',
                                                                                                                                                                                                                                                                'port': 5432,
                                                                                                                                                                                                                                                                'replicas': [
                                                                                                                                                                                                                                                                    {'host': 'db-replica-1.internal', 'port': 5432},
                                                                                                                                                                                                                                                                    {'host': 'db-replica-2.internal', 'port': 5432},
                                                                                                                                                                                                                                                                ],
                                                                                                                                                                                                                                                            },
                                                                                                                                                                                                                                                            'cache': {
                                                                                                                                                                                                                                                                'host': 'cache.internal',
                                                                                                                                                                                                                                                                'port': 6379,
                                                                                                                                                                                                                                                                'enabled': True,
                                                                                                                                                                                                                                                            },
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                        'feature_flags': {
                                                                                                                                                                                                                                                            'new_dashboard': True,
                                                                                                                                                                                                                                                            'beta_search': False,
                                                                                                                                                                                                                                                            'experimental': {
                                                                                                                                                                                                                                                                'group_a': {'enabled': True, 'rollout': 0.25},
                                                                                                                                                                                                                                                                'group_b': {'enabled': False, 'rollout': 0.0},
                                                                                                                                                                                                                                                            },
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                    'graph': {
                                                                                                                                                                                                                                                        'nodes': {
                                                                                                                                                                                                                                                            'n1': {'label': 'Start'},
                                                                                                                                                                                                                                                            'n2': {'label': 'Process'},
                                                                                                                                                                                                                                                            'n3': {'label': 'End'},
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                        'edges': [
                                                                                                                                                                                                                                                            ('n1', 'n2'),
                                                                                                                                                                                                                                                            ('n2', 'n3'),
                                                                                                                                                                                                                                                        ],
                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                    'mixed_values': [
                                                                                                                                                                                                                                                        None,
                                                                                                                                                                                                                                                        True,
                                                                                                                                                                                                                                                        False,
                                                                                                                                                                                                                                                        123,
                                                                                                                                                                                                                                                        45.67,
                                                                                                                                                                                                                                                        'hello world',
                                                                                                                                                                                                                                                        b'binary-data',
                                                                                                                                                                                                                                                        [1, 2, {'a': [3, 4, {'b': 5}]}],
                                                                                                                                                                                                                                                        (
                                                                                                                                                                                                                                                            {'x', 'y', 'z'},
                                                                                                                                                                                                                                                            {'nested': ('tuple', {'inside': 'dict'})},
                                                                                                                                                                                                                                                        ),
                                                                                                                                                                                                                                                    ],
                                                                                                                                                                                                                                                }]}],
            (
                {'x', 'y', 'z'},
                {'nested': ('tuple', {'inside': 'dict'})},
            ),
        ],
    }
    
    expected = {
        'metadata': {
            'version': 3,
            'created': '2026-06-08T12:34:56Z',
            'active': True,
            'tags': {'demo', 'nested', 'complex', 'python'},
            'checksum': None,
        },
        'users': [
            {
                'id': 1001,
                'name': 'Alice',
                'age': 31,
                'scores': [98, 87, 91],
                'preferences': {
                    'theme': 'dark',
                    'notifications': {
                        'email': True,
                        'sms': False,
                        'push': True,
                    },
                    'favorite_numbers': (3, 7, 11, 13),
                },
                'addresses': [
                    {
                        'type': 'home',
                        'location': {
                            'country': 'USA',
                            'city': 'Seattle',
                            'coordinates': (47.6062, -122.3321),
                        },
                    },
                    {
                        'type': 'work',
                        'location': {
                            'country': 'USA',
                            'city': 'Bellevue',
                            'coordinates': (47.6101, -122.2015),
                        },
                    },
                ],
            },
            {
                'id': 1002,
                'name': 'Bob',
                'age': 27,
                'scores': [76, 82, 89],
                'preferences': {
                    'theme': 'light',
                    'notifications': {
                        'email': False,
                        'sms': True,
                        'push': False,
                    },
                    'favorite_numbers': (2, 4, 8, 16),
                },
                'addresses': [],
            },
        ],
        'inventory': {
            'warehouse_a': {
                'items': [
                    {
                        'sku': 'A-001',
                        'name': 'Widget',
                        'price': 19.99,
                        'stock': 500,
                        'attributes': {
                            'colors': ['red', 'blue', 'green'],
                            'sizes': ['S', 'M', 'L'],
                            'dimensions': {
                                'width': 12.5,
                                'height': 8.0,
                                'depth': 4.2,
                            },
                        },
                    },
                    {
                        'sku': 'A-002',
                        'name': 'Gadget',
                        'price': 49.95,
                        'stock': 125,
                        'attributes': {
                            'colors': ['black'],
                            'sizes': [],
                            'dimensions': {
                                'width': 20.0,
                                'height': 5.0,
                                'depth': 2.5,
                            },
                        },
                    },
                ]
            },
            'warehouse_b': {
                'items': [],
                'capacity': 10000,
            },
        },
        'analytics': {
            'daily': [
                {'date': '2026-06-01', 'visits': 10234, 'conversion': 0.034},
                {'date': '2026-06-02', 'visits': 11287, 'conversion': 0.031},
                {'date': '2026-06-03', 'visits': 10891, 'conversion': 0.036},
            ],
            'aggregates': {
                'total_visits': 32412,
                'average_conversion': 0.0337,
                'histogram': {
                    '0-10': 12,
                    '10-20': 33,
                    '20-30': 25,
                    '30+': 8,
                },
            },
        },
        'configuration': {
            'services': {
                'database': {
                    'host': 'db.internal',
                    'port': 5432,
                    'replicas': [
                        {'host': 'db-replica-1.internal', 'port': 5432},
                        {'host': 'db-replica-2.internal', 'port': 5432},
                    ],
                },
                'cache': {
                    'host': 'cache.internal',
                    'port': 6379,
                    'enabled': True,
                },
            },
            'feature_flags': {
                'new_dashboard': True,
                'beta_search': False,
                'experimental': {
                    'group_a': {'enabled': True, 'rollout': 0.25},
                    'group_b': {'enabled': False, 'rollout': 0.0},
                },
            },
        },
        'graph': {
            'nodes': {
                'n1': {'label': 'Start'},
                'n2': {'label': 'Process'},
                'n3': {'label': 'End'},
            },
            'edges': [
                ('n1', 'n2'),
                ('n2', 'n3'),
            ],
        },
        'mixed_values': [
            None,
            True,
            False,
            123,
            45.67,
            'hello world',
            b'binary-data',
            [1, 2, {'a': [3, 4, {'b': 5}, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, {
                                                                                                                                                                                                                                                    'metadata': {
                                                                                                                                                                                                                                                        'version': 3,
                                                                                                                                                                                                                                                        'created': '2026-06-08T12:34:56Z',
                                                                                                                                                                                                                                                        'active': True,
                                                                                                                                                                                                                                                        'tags': {'demo', 'nested', 'complex', 'python', },
                                                                                                                                                                                                                                                        'checksum': None,
                                                                                                                                                                                                                                                        'NEST_1': {
                                                                                                                                                                                                                                                            'NEST_2': {
                                                                                                                                                                                                                                                                'NEST_3': {
                                                                                                                                                                                                                                                                    'NEST_4': {
                                                                                                                                                                                                                                                                        'NEST_5': {
                                                                                                                                                                                                                                                                            'NEST_6': {
                                                                                                                                                                                                                                                                                'NEST_7': {
                                                                                                                                                                                                                                                                                    'NEST_8': {
                                                                                                                                                                                                                                                                                        'NEST_9': {
                                                                                                                                                                                                                                                                                            'NEST_1': {
                                                                                                                                                                                                                                                                                                'NEST_2': {
                                                                                                                                                                                                                                                                                                    'NEST_3': {
                                                                                                                                                                                                                                                                                                        'NEST_4': {
                                                                                                                                                                                                                                                                                                            'NEST_5': {
                                                                                                                                                                                                                                                                                                                'NEST_6': {
                                                                                                                                                                                                                                                                                                                    'NEST_7': {
                                                                                                                                                                                                                                                                                                                        'NEST_8': {
                                                                                                                                                                                                                                                                                                                            'NEST_9': {
                                                                                                                                                                                                                                                                                                                                'NEST_1': {
                                                                                                                                                                                                                                                                                                                                    'NEST_2': {
                                                                                                                                                                                                                                                                                                                                        'NEST_3': {
                                                                                                                                                                                                                                                                                                                                            'NEST_4': {
                                                                                                                                                                                                                                                                                                                                                'NEST_5': {
                                                                                                                                                                                                                                                                                                                                                    'NEST_6': {
                                                                                                                                                                                                                                                                                                                                                        'NEST_7': {
                                                                                                                                                                                                                                                                                                                                                            'NEST_8': {
                                                                                                                                                                                                                                                                                                                                                                'NEST_9': {
                                                                                                                                                                                                                                                                                                                                                                    'EDGE': 'I AM THE REAL EDGE EDGE'
                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                        }

                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                    'users': [
                                                                                                                                                                                                                                                        {   
                                                                                                                                                                                                                                                            'fake_user': 'I could be free … If I could pluck out the memory of him from my heart as easily as his heart was plucked from the fire, I could be free. I discover that grief means living with someone who is no longer there. The Buddhists believe that our returning spirit XXXXXXXXXXXXXXXXX may inhabit any form it chooses. Is that him? Mistletoe on the winter oak. Is that him? Swooping above me in the body of a bird. I could wear him on my finger in the ring he gave me. If I rub it, will he appear again in human form?',
                                                                                                                                                                                                                                                            'id': 1001,
                                                                                                                                                                                                                                                            'name': 'Alice',
                                                                                                                                                                                                                                                            'age': 31,
                                                                                                                                                                                                                                                            'scores': [98, 87, 91],
                                                                                                                                                                                                                                                            'preferences': {
                                                                                                                                                                                                                                                                'theme': 'dark',
                                                                                                                                                                                                                                                                'notifications': {
                                                                                                                                                                                                                                                                    'email': True,
                                                                                                                                                                                                                                                                    'sms': False,
                                                                                                                                                                                                                                                                    'push': True,
                                                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                                                'favorite_numbers': (3, 7, 11, 13),
                                                                                                                                                                                                                                                            },
                                                                                                                                                                                                                                                            'addresses': [
                                                                                                                                                                                                                                                                {
                                                                                                                                                                                                                                                                    'type': 'home',
                                                                                                                                                                                                                                                                    'location': {
                                                                                                                                                                                                                                                                        'country': 'USA',
                                                                                                                                                                                                                                                                        'city': 'Seattle',
                                                                                                                                                                                                                                                                        'coordinates': (47.6062, -122.3321),
                                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                                                {
                                                                                                                                                                                                                                                                    'type': 'work',
                                                                                                                                                                                                                                                                    'location': {
                                                                                                                                                                                                                                                                        'country': 'USA',
                                                                                                                                                                                                                                                                        'city': 'Bellevue',
                                                                                                                                                                                                                                                                        'coordinates': (47.6101, -122.2015),
                                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                                            ],
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                        {
                                                                                                                                                                                                                                                            'id': 1002,
                                                                                                                                                                                                                                                            'name': 'Bob',
                                                                                                                                                                                                                                                            'age': 27,
                                                                                                                                                                                                                                                            'scores': [76, 82, 89],
                                                                                                                                                                                                                                                            'preferences': {
                                                                                                                                                                                                                                                                'theme': 'light',
                                                                                                                                                                                                                                                                'notifications': {
                                                                                                                                                                                                                                                                    'email': False,
                                                                                                                                                                                                                                                                    'sms': True,
                                                                                                                                                                                                                                                                    'push': False,
                                                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                                                'favorite_numbers': (2, 4, 8, 16),
                                                                                                                                                                                                                                                            },
                                                                                                                                                                                                                                                            'addresses': [],
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                    ],
                                                                                                                                                                                                                                                    'inventory': {
                                                                                                                                                                                                                                                        'warehouse_a': {
                                                                                                                                                                                                                                                            'items': [
                                                                                                                                                                                                                                                                {
                                                                                                                                                                                                                                                                    'sku': 'A-001',
                                                                                                                                                                                                                                                                    'name': 'Widget',
                                                                                                                                                                                                                                                                    'price': 19.99,
                                                                                                                                                                                                                                                                    'stock': 500,
                                                                                                                                                                                                                                                                    'attributes': {
                                                                                                                                                                                                                                                                        'colors': ['red', 'blue', 'green'],
                                                                                                                                                                                                                                                                        'sizes': ['S', 'M', 'L'],
                                                                                                                                                                                                                                                                        'dimensions': {
                                                                                                                                                                                                                                                                            'width': 12.5,
                                                                                                                                                                                                                                                                            'height': 8.0,
                                                                                                                                                                                                                                                                            'depth': 4.2,
                                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                                                {
                                                                                                                                                                                                                                                                    'sku': 'A-002',
                                                                                                                                                                                                                                                                    'name': 'Gadget',
                                                                                                                                                                                                                                                                    'price': 49.95,
                                                                                                                                                                                                                                                                    'stock': 125,
                                                                                                                                                                                                                                                                    'attributes': {
                                                                                                                                                                                                                                                                        'colors': ['black'],
                                                                                                                                                                                                                                                                        'sizes': [],
                                                                                                                                                                                                                                                                        'dimensions': {
                                                                                                                                                                                                                                                                            'width': 20.0,
                                                                                                                                                                                                                                                                            'height': 5.0,
                                                                                                                                                                                                                                                                            'depth': 2.5,
                                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                                            ]
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                        'warehouse_b': {
                                                                                                                                                                                                                                                            'items': [],
                                                                                                                                                                                                                                                            'capacity': 10000,
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                    'analytics': {
                                                                                                                                                                                                                                                        'daily': [
                                                                                                                                                                                                                                                            {'date': '2026-06-01', 'visits': 10234, 'conversion': 0.034},
                                                                                                                                                                                                                                                            {'date': '2026-06-02', 'visits': 11287, 'conversion': 0.031},
                                                                                                                                                                                                                                                            {'date': '2026-06-03', 'visits': 10891, 'conversion': 0.036},
                                                                                                                                                                                                                                                        ],
                                                                                                                                                                                                                                                        'aggregates': {
                                                                                                                                                                                                                                                            'total_visits': 32412,
                                                                                                                                                                                                                                                            'average_conversion': 0.0337,
                                                                                                                                                                                                                                                            'histogram': {
                                                                                                                                                                                                                                                                '0-10': 12,
                                                                                                                                                                                                                                                                '10-20': 33,
                                                                                                                                                                                                                                                                '20-30': 25,
                                                                                                                                                                                                                                                                '30+': 8,
                                                                                                                                                                                                                                                            },
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                    'configuration': {
                                                                                                                                                                                                                                                        'services': {
                                                                                                                                                                                                                                                            'database': {
                                                                                                                                                                                                                                                                'host': 'db.internal',
                                                                                                                                                                                                                                                                'port': 5432,
                                                                                                                                                                                                                                                                'replicas': [
                                                                                                                                                                                                                                                                    {'host': 'db-replica-1.internal', 'port': 5432},
                                                                                                                                                                                                                                                                    {'host': 'db-replica-2.internal', 'port': 5432},
                                                                                                                                                                                                                                                                ],
                                                                                                                                                                                                                                                            },
                                                                                                                                                                                                                                                            'cache': {
                                                                                                                                                                                                                                                                'host': 'cache.internal',
                                                                                                                                                                                                                                                                'port': 6379,
                                                                                                                                                                                                                                                                'enabled': True,
                                                                                                                                                                                                                                                            },
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                        'feature_flags': {
                                                                                                                                                                                                                                                            'new_dashboard': True,
                                                                                                                                                                                                                                                            'beta_search': False,
                                                                                                                                                                                                                                                            'experimental': {
                                                                                                                                                                                                                                                                'group_a': {'enabled': True, 'rollout': 0.25},
                                                                                                                                                                                                                                                                'group_b': {'enabled': False, 'rollout': 0.0},
                                                                                                                                                                                                                                                            },
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                    'graph': {
                                                                                                                                                                                                                                                        'nodes': {
                                                                                                                                                                                                                                                            'n1': {'label': 'Start'},
                                                                                                                                                                                                                                                            'n2': {'label': 'Process'},
                                                                                                                                                                                                                                                            'n3': {'label': 'End'},
                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                        'edges': [
                                                                                                                                                                                                                                                            ('n1', 'n2'),
                                                                                                                                                                                                                                                            ('n2', 'n3'),
                                                                                                                                                                                                                                                        ],
                                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                                    'mixed_values': [
                                                                                                                                                                                                                                                        None,
                                                                                                                                                                                                                                                        True,
                                                                                                                                                                                                                                                        False,
                                                                                                                                                                                                                                                        123,
                                                                                                                                                                                                                                                        45.67,
                                                                                                                                                                                                                                                        'hello world',
                                                                                                                                                                                                                                                        b'binary-data',
                                                                                                                                                                                                                                                        [1, 2, {'a': [3, 4, {'b': 5}]}],
                                                                                                                                                                                                                                                        (
                                                                                                                                                                                                                                                            {'x', 'y', 'z'},
                                                                                                                                                                                                                                                            {'nested': ('tuple', {'inside': 'dict'})},
                                                                                                                                                                                                                                                        ),
                                                                                                                                                                                                                                                    ],
                                                                                                                                                                                                                                                }]}],
            (
                {'x', 'y', 'z'},
                {'nested': ('tuple', {'inside': 'dict'})},
            ),
        ],
    }

    ## 
    offset = 100
    mult = 100
    actual_big_text = actual['mixed_values'][7][2]['a'][70]['users'][0]['fake_user']
    actual['mixed_values'][7][2]['a'][70]['users'][0]['fake_user'] = mult * actual_big_text[:offset] + actual_big_text[offset:-offset] + mult * actual_big_text[-offset:]

    expected_big_text = expected['mixed_values'][7][2]['a'][70]['users'][0]['fake_user']
    expected['mixed_values'][7][2]['a'][70]['users'][0]['fake_user'] = mult * expected_big_text[:offset] + expected_big_text[offset:-offset] + mult * expected_big_text[-offset:]


    actual_metadata = actual['mixed_values'][7][2]['a'][70]['metadata']
    expected_metadata = expected['mixed_values'][7][2]['a'][70]['metadata']
    del actual['mixed_values'][7][2]['a'][70]['metadata']
    del expected['mixed_values'][7][2]['a'][70]['metadata']

    # Test single line 
    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(actual, expected)  
    
    must_equal(r'''
ITEM['mixed_values'][7][2]['a'][70]['users'][0]['fake_user']:
string mismatch at index 10158
expected char: 'm'
actual char:   'X'

expected: ' believe that our returning spirit may inhabit any form it chooses. Is'
actual:   ' believe that our returning spirit XXXXXXXXXXXXXXXXX may inhabit any f'
                                              ^
[EOD]''', str(context.exception))  

    
    # Test multi line 
    def fake_data(data: str, mod: bool, add_new_line: bool = True) ->  str:
        new_data = []
        for idx in range(100, len(data), 100):
            if mod:
                new_data.append(data[idx-100:idx]+'--DIFF--')
            else:
                new_data.append(data[idx-100:idx])
        return '\n'.join(new_data)
    

    
    actual['mixed_values'][7][2]['a'][70]['users'][0]['fake_user'] = fake_data(actual['mixed_values'][7][2]['a'][70]['users'][0]['fake_user'], False)
    
    # remove initial diff from expected  .replace('XXXXXXXXXXXXXXXXX ')
    expected['mixed_values'][7][2]['a'][70]['users'][0]['fake_user'] = fake_data(str(expected['mixed_values'][7][2]['a'][70]['users'][0]['fake_user']).replace('XXXXXXXXXXXXXXXXX ', ''), True)
    
    # print(actual['mixed_values'][7][2]['a'][70]['users'][0]['fake_user'])
    # print('----------')
    # print(expected['mixed_values'][7][2]['a'][70]['users'][0]['fake_user'])
    

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(actual, expected)  
    
    must_equal(r'''
ITEM['mixed_values'][7][2]['a'][70]['users'][0]['fake_user']:
--- expected
+++ actual

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -1,202 +1,202 @@

~~~~~~~~~~~~~~~~~~~~~~~~

string mismatch at index 100
expected char: '\n'
actual char:   '-'

expected: 'heart as easily as his heart was pl\n'
actual:   'heart as easily as his heart was pl--DIFF--\n'
                                              ^

string mismatch at index 100
expected char: '\n'
actual char:   '-'

expected: 'heart as easily as his heart was pl\n'
actual:   'heart as easily as his heart was pl--DIFF--\n'
                                              ^

string mismatch at index 100
expected char: '\n'
actual char:   '-'

expected: 'heart as easily as his heart was pl\n'
actual:   'heart as easily as his heart was pl--DIFF--\n'
                                              ^

[EOD]''', str(context.exception))



    del actual['mixed_values'][7][2]['a'][70]['users'][0]['fake_user']
    del expected['mixed_values'][7][2]['a'][70]['users'][0]['fake_user']
    # Test nest
    actual['mixed_values'][7][2]['a'][70]['metadata'] = actual_metadata
    expected['mixed_values'][7][2]['a'][70]['metadata'] = expected_metadata


    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(actual=actual['mixed_values'], expected=expected['mixed_values'])   
                                                                                                                             
    must_equal(r'''
ITEM[7][2]['a'][70]['metadata']['NEST_1']['NEST_2']['NEST_3']['NEST_4']['NEST_5']['NEST_6']['NEST_7']['NEST_8']['NEST_9']['NEST_1']['NEST_2']['NEST_3']['NEST_4']['NEST_5']['NEST_6']['NEST_7']['NEST_8']['NEST_9']['NEST_1']['NEST_2']['NEST_3']['NEST_4']['NEST_5']['NEST_6']['NEST_7']['NEST_8']['NEST_9']['EDGE']:
string mismatch at index 9
expected char: 'R'
actual char:   'E'

expected: 'I AM THE REAL EDGE EDGE'
actual:   'I AM THE EDGE'
                    ^
[EOD]''', str(context.exception))