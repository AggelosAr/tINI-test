from tini_test import Isolate, Mock, Test, must_equal

X = 10
Y = 10
UPDATED = {'X', 'Y'}


def closure_as_function(x):

    def inner():
        return x + 100

    return inner()


def closure_with_namny_args(*args, **kwargs):

    def inner():
        return sum(args) + sum(kwargs.values())

    return inner()


def closure_with_global_defined(*args):

    def inner():
        global X
        res = X + 10
        return res

    return inner()



def closure_with_global(*args):

    def inner():
        res = X + 10
        return res

    return inner()


def combination_closure(y):

    def inner():
        global Y
        res = Y + y
        return res

    return inner()



def closure_with_free_var(x):

    def inner(y):
        return x + y

    return inner(x)



def closure_modify_global_X():

    def inner():
        UPDATED.discard('X')

    return inner()


def closure_modify_global_Y():

    def inner():
        UPDATED.discard('Y')

    return inner()



def closure_with_class(arg1):

    class Inner:
        def __init__(self, _value_a, _value_b):
            self._value_a = _value_a
            self._value_b = _value_b


    def inner(arg2):
        obj = Inner(arg1, arg2)
        return obj

    arg2 = 'X'
    return inner(arg2)



#######################################


@Isolate
@Test.case
@Mock.mock(closure_as_function, args=(5,))
def test_closure_as_function():
    must_equal(100 + 5, closure_as_function('?'))
    must_equal(100 + 5, closure_as_function('?'))
    must_equal(100 + 5, closure_as_function('?'))


    # must_equal(100 + 1, closure_as_function(1))
    must_equal(1 + 1, closure_with_namny_args(1, a=1))
    must_equal(20, closure_with_global_defined())
    must_equal(20, closure_with_global())
    must_equal(20, combination_closure(10))
    must_equal(5 + 5, closure_with_free_var(5))



@Isolate
@Test.case
@Mock.mock(closure_with_namny_args, args=(1, 1), kwargs={'a': 1, 'b': 1})
def test_closure_with_namny_args():
    must_equal(4, closure_with_namny_args('?'))
    must_equal(4, closure_with_namny_args('?'))
    must_equal(4, closure_with_namny_args('?'))

    must_equal(100 + 1, closure_as_function(1))
    # must_equal(1 + 1, closure_with_namny_args(1, a=1))
    must_equal(20, closure_with_global_defined())
    must_equal(20, closure_with_global())
    must_equal(20, combination_closure(10))
    must_equal(5 + 5, closure_with_free_var(5))




@Isolate
@Test.case
@Mock.mock(closure_with_global_defined, args=(5,))
def test_closure_with_global_defined():
    must_equal(20, closure_with_global_defined('?'))
    must_equal(20, closure_with_global_defined('?'))
    must_equal(20, closure_with_global_defined('?'))

    must_equal(100 + 1, closure_as_function(1))
    must_equal(1 + 1, closure_with_namny_args(1, a=1))
    # must_equal(20, closure_with_global_defined())
    must_equal(20, closure_with_global())
    must_equal(20, combination_closure(10))
    must_equal(5 + 5, closure_with_free_var(5))




@Isolate
@Test.case
@Mock.mock(closure_with_global, args=(5,))
def test_closure_with_global():
    must_equal(20, closure_with_global('?'))
    must_equal(20, closure_with_global('?'))
    must_equal(20, closure_with_global('?'))

    must_equal(100 + 1, closure_as_function(1))
    must_equal(1 + 1, closure_with_namny_args(1, a=1))
    must_equal(20, closure_with_global_defined())
    # must_equal(20, closure_with_global())
    must_equal(20, combination_closure(10))
    must_equal(5 + 5, closure_with_free_var(5))




@Isolate
@Test.case
@Mock.mock(combination_closure, args=(5,))
def test_combination_closure():
    must_equal(15, combination_closure('?')) 
    must_equal(15, combination_closure('?')) 
    must_equal(15, combination_closure('?'))  

    must_equal(100 + 1, closure_as_function(1))
    must_equal(1 + 1, closure_with_namny_args(1, a=1))
    must_equal(20, closure_with_global_defined())
    must_equal(20, closure_with_global())
    # must_equal(20, combination_closure(10))
    must_equal(5 + 5, closure_with_free_var(5))



@Isolate
@Test.case
@Mock.mock(closure_with_free_var, args=(5,))
def test_closure_with_free_var():
    must_equal(5 + 5, closure_with_free_var('?')) 
    must_equal(5 + 5, closure_with_free_var('?')) 
    must_equal(5 + 5, closure_with_free_var('?'))  

    must_equal(100 + 1, closure_as_function(1))
    must_equal(1 + 1, closure_with_namny_args(1, a=1))
    must_equal(20, closure_with_global_defined())
    must_equal(20, closure_with_global())
    must_equal(20, combination_closure(10))
    # must_equal(5 + 5, closure_with_free_var(5))



@Isolate
@Test.case
@Mock.mock(closure_modify_global_X, args=())
def test_closure_modify_global():
    closure_modify_global_X()
    must_equal(False, 'X' in UPDATED)



@Isolate
@Test.case
@Mock.mock(closure_modify_global_Y, returns=100)
def test_closure_modify_global_Y():
    must_equal(100, closure_modify_global_Y())
    must_equal(True, 'Y' in UPDATED)


@Isolate
@Test.case
@Mock.mock(closure_with_class, args=('100',))
def test_closure_with_class():
    obj = closure_with_class('?')
    must_equal('100', obj._value_a)
    must_equal('X', obj._value_b)




################# IMPORTED 
from all_tests.test_about_mocks.test_mocks.tests.import_a.import_b.import_c.closure_mock_utils import (
    imported_closure_as_function, imported_closure_modify_global_X,
    imported_closure_modify_global_Y, imported_closure_with_class,
    imported_closure_with_free_var, imported_closure_with_global,
    imported_closure_with_global_defined, imported_closure_with_namny_args,
    imported_combination_closure)


@Isolate
@Test.case
@Mock.mock(imported_closure_as_function, args=(5,))
def imported_test_closure_as_function():
    must_equal(100 + 5, imported_closure_as_function('?'))
    must_equal(100 + 5, imported_closure_as_function('?'))
    must_equal(100 + 5, imported_closure_as_function('?'))


    # must_equal(100 + 1, closure_as_function(1))
    must_equal(1 + 1, imported_closure_with_namny_args(1, a=1))
    must_equal(20, imported_closure_with_global_defined())
    must_equal(20, imported_closure_with_global())
    must_equal(20, imported_combination_closure(10))
    must_equal(5 + 5, imported_closure_with_free_var(5))



@Isolate
@Test.case
@Mock.mock(imported_closure_with_namny_args, args=(1, 1), kwargs={'a': 1, 'b': 1})
def imported_test_closure_with_namny_args():
    must_equal(4, imported_closure_with_namny_args('?'))
    must_equal(4, imported_closure_with_namny_args('?'))
    must_equal(4, imported_closure_with_namny_args('?'))

    must_equal(100 + 1, imported_closure_as_function(1))
    # must_equal(1 + 1, imported_closure_with_namny_args(1, a=1))
    must_equal(20, imported_closure_with_global_defined())
    must_equal(20, imported_closure_with_global())
    must_equal(20, imported_combination_closure(10))
    must_equal(5 + 5, imported_closure_with_free_var(5))




@Isolate
@Test.case
@Mock.mock(imported_closure_with_global_defined, args=(5,))
def imported_test_closure_with_global_defined():
    must_equal(20, imported_closure_with_global_defined('?'))
    must_equal(20, imported_closure_with_global_defined('?'))
    must_equal(20, imported_closure_with_global_defined('?'))

    must_equal(100 + 1, imported_closure_as_function(1))
    must_equal(1 + 1, imported_closure_with_namny_args(1, a=1))
    # must_equal(20, imported_closure_with_global_defined())
    must_equal(20, imported_closure_with_global())
    must_equal(20, imported_combination_closure(10))
    must_equal(5 + 5, imported_closure_with_free_var(5))




@Isolate
@Test.case
@Mock.mock(imported_closure_with_global, args=(5,))
def imported_test_closure_with_global():
    must_equal(20, imported_closure_with_global('?'))
    must_equal(20, imported_closure_with_global('?'))
    must_equal(20, imported_closure_with_global('?'))

    must_equal(100 + 1, imported_closure_as_function(1))
    must_equal(1 + 1, imported_closure_with_namny_args(1, a=1))
    must_equal(20, imported_closure_with_global_defined())
    # must_equal(20, imported_closure_with_global())
    must_equal(20, imported_combination_closure(10))
    must_equal(5 + 5, imported_closure_with_free_var(5))




@Isolate
@Test.case
@Mock.mock(imported_combination_closure, args=(5,))
def imported_test_combination_closure():
    must_equal(15, imported_combination_closure('?')) 
    must_equal(15, imported_combination_closure('?')) 
    must_equal(15, imported_combination_closure('?'))  

    must_equal(100 + 1, imported_closure_as_function(1))
    must_equal(1 + 1, imported_closure_with_namny_args(1, a=1))
    must_equal(20, imported_closure_with_global_defined())
    must_equal(20, imported_closure_with_global())
    # must_equal(20, imported_combination_closure(10))
    must_equal(5 + 5, imported_closure_with_free_var(5))



@Isolate
@Test.case
@Mock.mock(imported_closure_with_free_var, args=(5,))
def imported_test_closure_with_free_var():
    must_equal(5 + 5, imported_closure_with_free_var('?')) 
    must_equal(5 + 5, imported_closure_with_free_var('?')) 
    must_equal(5 + 5, imported_closure_with_free_var('?'))  

    must_equal(100 + 1, imported_closure_as_function(1))
    must_equal(1 + 1, imported_closure_with_namny_args(1, a=1))
    must_equal(20, imported_closure_with_global_defined())
    must_equal(20, imported_closure_with_global())
    must_equal(20, imported_combination_closure(10))
    # must_equal(5 + 5, imported_closure_with_free_var(5))



@Isolate
@Test.case
@Mock.mock(imported_closure_modify_global_X, args=())
def imported_test_closure_modify_global():
    from all_tests.test_about_mocks.test_mocks.tests.import_a.import_b.import_c.closure_mock_utils import \
        UPDATED as u
    imported_closure_modify_global_X()
    must_equal(False, 'X' in u)



@Isolate
@Test.case
@Mock.mock(imported_closure_modify_global_Y, returns=100)
def imported_test_closure_modify_global_Y():
    must_equal(100, imported_closure_modify_global_Y())
    from all_tests.test_about_mocks.test_mocks.tests.import_a.import_b.import_c.closure_mock_utils import \
        UPDATED as u  # did this break isort? who knows ....
    must_equal(True, 'Y' in u)


@Isolate
@Test.case
@Mock.mock(imported_closure_with_class, args=('100',))
def imported_test_closure_with_class():
    obj = imported_closure_with_class('?')
    must_equal('100', obj._value_a)
    must_equal('X', obj._value_b)