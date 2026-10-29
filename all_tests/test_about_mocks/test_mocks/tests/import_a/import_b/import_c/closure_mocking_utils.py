import os

from all_tests.test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
    ___test_mocked_function
from tini_test import Mock, must_equal, var


def ___test_mocking_in_outside_function(*args, **kwargs):
    with Mock.mocking(___test_mocked_function, args=(5, 5), kwargs={'k_val_1': 5}):
        result = ___test_mocked_function('?')
    must_equal(15, result)
    return result



def test_imported_x_function(num: int, use_mock: bool):
  
    def function_x(arg2):
        return num + arg2
    
    if use_mock:
        with Mock.mocking(function_x, args=(100,)):

            return function_x('?')
       

    if not use_mock:

        return function_x(200)



def test_imported_builtin_open(_path: str, use_mock: bool):

    if use_mock:
        with Mock.mocking(open, args=(os.path.join(var.root, _path), 'r')):

            with open('?') as f:
                content = f.read()
       
        return content

    if not use_mock:

        with open(os.path.join(var.root, _path), 'r') as f:
            content = f.read()

        return content






#######################

X = 10
Y = 10
UPDATED = {'X', 'Y'}



def imported_closure_with_namny_args(*args, **kwargs):

    def inner():
        return sum(args) + sum(kwargs.values())


    with Mock.mocking(inner, returns=4):
        return inner()



def imported_closure_with_global_defined(*args):

    def inner():
        global X
        res = X + 10
        return res

    with Mock.mocking(inner, returns=4):
        return inner()



def imported_closure_with_global(*args):

    def inner():
        res = X + 10
        return res

    with Mock.mocking(inner, returns=4):
        return inner()


def imported_combination_closure(y):

    def inner():
        global Y
        res = Y + y
        return res
    
    with Mock.mocking(inner, returns=4):
        return inner()



def imported_closure_with_free_var(x):

    def inner(y):
        return x + y

    with Mock.mocking(inner, args=(4,)):
        return inner(x)



def imported_closure_modify_global_X():

    def inner():
        UPDATED.discard('X')

    with Mock.mocking(inner, returns=None):
        return inner()



def imported_closure_modify_global_Y():

    def inner(args):
        must_equal(100, args)
        UPDATED.discard('Y')

    with Mock.mocking(inner, args=(100,)):
        return inner()




def imported_closure_with_class(arg1):

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






############################



def imported_nesting_closure_with_class():

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

            inst = inner('?')
            must_equal(22, inst._value_a)
            must_equal(2, inst._value_b)

            with Mock.mocking(inner, args=(3,)):

                var.a = 33
                inst = inner('?')
                must_equal(33, inst._value_a)
                must_equal(3, inst._value_b)

                inst = inner('?')
                must_equal(33, inst._value_a)
                must_equal(3, inst._value_b)

                with Mock.mocking(inner, args=(4,)):

                    var.a = 44
                    inst = inner('?')
                    must_equal(44, inst._value_a)
                    must_equal(4, inst._value_b)

                    inst = inner('?')
                    must_equal(44, inst._value_a)
                    must_equal(4, inst._value_b)
        

                var.a = 33
                inst = inner('?')
                must_equal(33, inst._value_a)
                must_equal(3, inst._value_b)

                inst = inner('?')
                must_equal(33, inst._value_a)
                must_equal(3, inst._value_b)

            var.a = 22
            inst = inner('?')
            must_equal(22, inst._value_a)
            must_equal(2, inst._value_b)

            inst = inner('?')
            must_equal(22, inst._value_a)
            must_equal(2, inst._value_b)

        var.a = 11
        inst = inner('?')
        must_equal(11, inst._value_a)
        must_equal(1, inst._value_b)

        inst = inner('?')
        must_equal(11, inst._value_a)
        must_equal(1, inst._value_b)

