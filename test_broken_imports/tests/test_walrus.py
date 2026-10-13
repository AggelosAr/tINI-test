
# '''

# ...........


# '''


# from dataclasses import dataclass

from tini_test.must_equals import must_equal
from tini_test.shared import NotInitialized, Shared, var
from tini_test.test_utils import Test


# [var.int]



@Shared(var.int)
@Test.case
def test_var_can_passed_as_armument_to_heavy_nest_function():
    must_equal(NotInitialized, var.int)
    var.int = 666
    ...
    




@Shared(var.int)
@Test.case
def test_var_can_passed_as_armument_to_heavy_nest_function():
    must_equal(NotInitialized, var.int)
    var.int = 666
    ...
   