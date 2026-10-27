from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.closure_mocking_utils import \
    test_imported_x_function
from tini_test import Isolate, Mock, Test, must_equal
from tini_test.shared import Shared, var

X = 10
Y = 10
UPDATED = {'X', 'Y'}


def closure_with_namny_args(*args, **kwargs):

    def inner():
        return sum(args) + sum(kwargs.values())


    with Mock.mocking(inner, returns=4):
        return inner()



def closure_with_global_defined(*args):

    def inner():
        global X
        res = X + 10
        return res

    with Mock.mocking(inner, returns=4):
        return inner()



def closure_with_global(*args):

    def inner():
        res = X + 10
        return res

    with Mock.mocking(inner, returns=4):
        return inner()


def combination_closure(y):

    def inner():
        global Y
        res = Y + y
        return res
    
    with Mock.mocking(inner, returns=4):
        return inner()



def closure_with_free_var(x):

    def inner(y):
        return x + y

    with Mock.mocking(inner, args=(4,)):
        return inner(x)



def closure_modify_global_X():

    def inner():
        UPDATED.discard('X')

    with Mock.mocking(inner, returns=None):
        return inner()



def closure_modify_global_Y():

    def inner(args):
        must_equal(100, args)
        UPDATED.discard('Y')

    with Mock.mocking(inner, args=(100,)):
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

    with Mock.mocking(inner, args=('OK',)):
        return inner(arg2)



#######################################

#######################################


@Isolate
@Test.case
def sanity_check():

    must_equal(1 + 100, test_imported_x_function(1, use_mock=True))

    must_equal(2 + 200, test_imported_x_function(2, use_mock=False))

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def test():
        from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.closure_mocking_utils import \
            test_imported_x_function
    
        must_equal(1 + 100, test_imported_x_function(1, use_mock=True))
    
        must_equal(2 + 200, test_imported_x_function(2, use_mock=False))

    test()
    test()

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////


#######################################

#######################################





@Isolate
@Test.case
def test_closure_with_namny_args():
    must_equal(4, closure_with_namny_args('?'))
    must_equal(4, closure_with_namny_args('?'))
    must_equal(4, closure_with_namny_args('?'))




@Isolate
@Test.case
def test_closure_with_global_defined():
    must_equal(4, closure_with_global_defined('?'))
    must_equal(4, closure_with_global_defined('?'))
    must_equal(4, closure_with_global_defined('?'))




@Isolate
@Test.case
def test_closure_with_global():
    must_equal(4, closure_with_global('?'))
    must_equal(4, closure_with_global('?'))
    must_equal(4, closure_with_global('?'))



@Isolate
@Test.case
def test_combination_closure():
    must_equal(4, combination_closure('?')) 
    must_equal(4, combination_closure('?')) 
    must_equal(4, combination_closure('?'))  

   


@Isolate
@Test.case
def test_closure_with_free_var():
    must_equal(111 + 4, closure_with_free_var(111)) 
    must_equal(111 + 4, closure_with_free_var(111)) 
    must_equal(111 + 4, closure_with_free_var(111))  




@Isolate
@Test.case
def test_closure_modify_global():
    closure_modify_global_X()
    must_equal(True, 'X' in UPDATED)



@Isolate
@Test.case
def test_closure_modify_global_Y():
    closure_modify_global_Y()
    must_equal(False, 'Y' in UPDATED)


@Isolate
@Test.case
def test_closure_with_class():
    obj = closure_with_class('?')
    must_equal('?', obj._value_a)
    must_equal('OK', obj._value_b)




################# IMPORTED 
from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.closure_mocking_utils import (
    imported_closure_modify_global_X, imported_closure_modify_global_Y,
    imported_closure_with_class, imported_closure_with_free_var,
    imported_closure_with_global, imported_closure_with_global_defined,
    imported_closure_with_namny_args, imported_combination_closure)


@Isolate
@Test.case
def imported_test_closure_with_namny_args():
    must_equal(4, imported_closure_with_namny_args('?'))
    must_equal(4, imported_closure_with_namny_args('?'))
    must_equal(4, imported_closure_with_namny_args('?'))




@Isolate
@Test.case
def imported_test_closure_with_global_defined():
    must_equal(4, imported_closure_with_global_defined('?'))
    must_equal(4, imported_closure_with_global_defined('?'))
    must_equal(4, imported_closure_with_global_defined('?'))




@Isolate
@Test.case
def imported_test_closure_with_global():
    must_equal(4, imported_closure_with_global('?'))
    must_equal(4, imported_closure_with_global('?'))
    must_equal(4, imported_closure_with_global('?'))



@Isolate
@Test.case
def imported_test_combination_closure():
    must_equal(4, imported_combination_closure('?')) 
    must_equal(4, imported_combination_closure('?')) 
    must_equal(4, imported_combination_closure('?'))  

   


@Isolate
@Test.case
def imported_test_closure_with_free_var():
    must_equal(111 + 4, imported_closure_with_free_var(111)) 
    must_equal(111 + 4, imported_closure_with_free_var(111)) 
    must_equal(111 + 4, imported_closure_with_free_var(111))  




@Isolate
@Test.case
def imported_test_closure_modify_global():
    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.closure_mocking_utils import \
        UPDATED as u
    imported_closure_modify_global_X()
    must_equal(True, 'X' in u)



@Isolate
@Test.case
def imported_test_closure_modify_global_Y():
    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.closure_mocking_utils import \
        UPDATED as u
    imported_closure_modify_global_Y()
    must_equal(False, 'Y' in u)


@Isolate
@Test.case
def imported_test_closure_with_class():
    obj = imported_closure_with_class('?')
    must_equal('?', obj._value_a)
    must_equal('OK', obj._value_b)



# Also add test with nesting 


def nesting_closure_with_class():

    class Inner:
        def __init__(self, _value_a, _value_b):
            self._value_a = _value_a
            self._value_b = _value_b


    def inner(arg2):
        obj = Inner(var.a, arg2)
        return obj

    arg2 = '?'

    
    with Mock.mocking(inner, args=(1,)):

        var.a = 11
        inst = inner('?')

        must_equal(11, inst._value_a)
        must_equal(1, inst._value_b)

        with Mock.mocking(inner, args=(2,)):

            var.a = 22
            inst = inner('?')
            must_equal(22, inst._value_a)
            must_equal(2, inst._value_b)

            with Mock.mocking(inner, args=(3,)):

                var.a = 33
                inst = inner('?')
                must_equal(33, inst._value_a)
                must_equal(3, inst._value_b)

                with Mock.mocking(inner, args=(4,)):

                    var.a = 44
                    inst = inner('?')
                    must_equal(44, inst._value_a)
                    must_equal(4, inst._value_b)
        

                var.a = 33
                inst = inner('?')
                must_equal(33, inst._value_a)
                must_equal(3, inst._value_b)

            var.a = 22
            inst = inner('?')
            must_equal(22, inst._value_a)
            must_equal(2, inst._value_b)

        var.a = 11
        inst = inner('?')
        must_equal(11, inst._value_a)
        must_equal(1, inst._value_b)



@Isolate
@Test.case
@Shared(var.a)
def test_nesting_closure_with_class():
    nesting_closure_with_class()
    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.closure_mocking_utils import \
        imported_nesting_closure_with_class
    imported_nesting_closure_with_class()
