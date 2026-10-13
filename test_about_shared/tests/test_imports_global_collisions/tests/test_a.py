from test_about_shared.tests.test_imports_global_collisions.tests.import_a.import_b.import_c.m_c import (
    _why_func_c, _why_func_c__C, func_c)
from test_about_shared.tests.test_imports_global_collisions.tests.import_a.import_b.m_b import \
    _why_func_b
from test_about_shared.tests.test_imports_global_collisions.tests.import_a.m_a import (
    _why_func_a, func_a)
from tini_test import NotInitialized, Shared, Test, must_equal, var


def test_example_a_helper():
    print('I am test example_a helper')


@Shared(var.int)
@Test.case
def test_var_can_passed_as_armument_to_heavy_nest_function():
    must_equal(NotInitialized, var.int)
    var.int = 666
    must_equal(666 + 2, func_a(var.int))
    must_equal(666 + 2, func_a(var.int))
    must_equal(666 + 2, func_a(var.int))




@Shared(var.int)
@Test.case
def test_var_can_passed_as_armument_to_heavy_nest_function_2():
    must_equal(NotInitialized, var.int)
    var.int = 666
    must_equal(666, func_c(var.int))
    must_equal(666, func_c(var.int))
    must_equal(666, func_c(var.int))




# ADD test .... if u try to use var without importing it, it breaks as expected.
@Shared(var.int)
@Test.case
def test_var_can_be_used_in_heavy_nest_function_without_import_in_the_nest_function():
    must_equal(NotInitialized, var.int)
    var.int = 666
    must_equal(666 + 666, _why_func_c(var.int))
    must_equal(666 + 666, _why_func_c(var.int))
    must_equal(666 + 666, _why_func_c(var.int))



@Shared(var.A, var.B, var.C)
@Test.case
def test_using_multiple_levels_of_nest():
    must_equal(NotInitialized, var.A)
    must_equal(NotInitialized, var.B)
    must_equal(NotInitialized, var.C)
    var.A = 111
    var.B = 222
    var.C = 333
    must_equal(111 + 222 + 333 + 1 + 1 + 1, _why_func_a(0))
    must_equal(222 + 333 + 1 + 1, _why_func_b(0))
    must_equal(333 + 1, _why_func_c__C(0))