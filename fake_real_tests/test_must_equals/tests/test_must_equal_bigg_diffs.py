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

expected: 'quat ullamco ea pariatur reprehenderit consectetur dolore est laboris. Consectetur aliqua consequat proident qui.\r\n'
actual:   'quat ullamco ea pariatur reprehenderit consectetur dolore est laboris. Consectetur aliqua consequat DIFFERENCE qui.\r\n'
                                                                                                               ^

''', str(context.exception))



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

expected: 'mco ea pariatur reprehenderit consectetur dolore est laboris. Consectetur aliqua consequat proident qui'
actual:   'mco ea pariatur reprehenderit consectetur dolore est laboris. Consectetur aliqua consequat proident DIFFERENCE'
                                                                                                               ^
''', str(context.exception))
    


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
  Consectetur fugiat nostrud excepteur id aliquip [TRUNCATED<5>chars]um deserunt nisi laborum eu ut commodo laboris ad
  Duis aliqua et labore ea
  Ad qui magna consectetur amet enim consequat ull[TRUNCATED<12>chars]atur reprehenderit consectetur dolore est laboris

string mismatch at index 39
expected char: 'q'
actual char:   'D'

expected: ' Consectetur aliqua consequat proident qui'
actual:   ' Consectetur aliqua consequat proident DIFFERENCE'
                                                  ^

''', str(context.exception))



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

expected: 'Officia in dolor excepteur ullamco sint.\n'
actual:   'YYYOfficia in dolor excepteur ullamco sint.\n'
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

''', str(context.exception))
    


@Test.case
def test_single_line_diff_weird_case() -> None:

    actual = 'ea pariatur reprehenderit consectetur dolore est laboris. Consectetur aliqua consequat proident qui.\r\n'
    expected = 'ea pariatur reprehenderit consectetur dolore est laboris. Consectetur aliqua consequat proident qui.\r\n'

    must_equal(actual, expected)



@Test.case
def xxxyyyzzz() -> None:

    must_equal('''
ITEM:
--- expected
+++ actual

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -1,4 +1,11 @@

~~~~~~~~~~~~~~~~~~~~~~~~

string mismatch at index 0
expected char: 'O'
actual char:   'Y'

expected: 'Officia in dolor excepteur ullamco sint.\n'
actual:   'YYYOfficia in dolor excepteur ullamco sint.\n'
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

''', '''
ITEM:
--- expected
+++ actual

~~~~~~~~~~~~~~~~~~~~~~~~
@@ -1,4 +1,11 @@

~~~~~~~~~~~~~~~~~~~~~~~~

string mismatch at index 0
expected char: 'O'
actual char:   'Y'

expected: 'Officia in dolor excepteur ullamco sint.\n'
actual:   'YYYOfficia in dolor excepteur ullamco sint.\n'
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