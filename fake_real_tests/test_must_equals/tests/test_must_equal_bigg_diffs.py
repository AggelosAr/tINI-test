import json

from small_test.context_manager import WillRaise
from small_test.misc.exceptions import ExpectedWasDifferentFromActual
from small_test.must_equals import must_equal
from small_test.test_utils import Test

import os

# TODO add a case in heavy nest in containers on the big json

@Test.case
def test_big_json_no_diff() -> None:
    
    root_path = '/home/papaggalos/workspace/python_projects/small_test/fake_real_tests/test_must_equals/tests'
    
    with open(os.path.join(root_path, 'json_expected.json')) as f:
        expected = json.load(f)

    with open(os.path.join(root_path, 'json_actual.json')) as f:
        actual = json.load(f)

    must_equal(expected, actual)



@Test.case
def test_big_json_diff() -> None:
    
    root_path = '/home/papaggalos/workspace/python_projects/small_test/fake_real_tests/test_must_equals/tests'
    
    with open(os.path.join(root_path, 'json_expected.json')) as f:
        expected = json.load(f)

    with open(os.path.join(root_path, 'json_actual_broken.json')) as f:
        actual = json.load(f)

    must_equal(expected, actual)



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

expected: 'tur aliqua consequat proident qui'
actual:   'tur aliqua consequat proident DIFFERENCE'
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

    print('--------------------')
    print(str(context.exception))
    print('--------------------')

    must_equal('''
ITEM:
--- expected
+++ actual
@@ -16,4 +16,4 @@
  Consectetur fugiat nostrud excepteur id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad
  Duis aliqua et labore ea
  Ad qui magna consectetur amet enim consequat ullamco ea pariatur reprehenderit consectetur dolore est laboris
- Consectetur aliqua consequat proident qui+ Consectetur aliqua consequat proident DIFFERENCE
''', str(context.exception))


@Test.case
def test_big_multi_line_string_diff_case() -> None:
    
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
    Consectetur fugiat nostrud excepteur id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad. 
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
    Officia in dolor excepteur ullamco sint.
    Ad qui magna consectetur amet enim consequat ullamco ea pariatur reprehenderit consectetur dolore est laboris. 
    Consectetur aliqua consequat proident qui'''

    actual = '''Officia in dolor excepteur ullamco sint.
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
    Consectetur fugiat nostrud DIFFFFFF id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad. 
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
    Officia in dolor excepteur ullamco sint.
    Ad qui magna consectetur amet enim consequat ullamco ea pariatur reprehenderit consectetur dolore est laboris. 
    Consectetur aliqua consequat proident qui'''
    
    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    print('--------------------')
    print(str(context.exception))
    print('--------------------')

    must_equal('''
ITEM:
--- expected
+++ actual
@@ -27,7 +27,7 @@
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
-    Consectetur fugiat nostrud excepteur id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.
+    Consectetur fugiat nostrud DIFFFFFF id aliquip laborum deserunt nisi laborum eu ut commodo laboris ad.
     Duis aliqua et labore ea.
     Officia in dolor excepteur ullamco sint.
     Officia in dolor excepteur ullamco sint.
''', str(context.exception))