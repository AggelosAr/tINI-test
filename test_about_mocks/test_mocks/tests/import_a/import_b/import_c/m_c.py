from tini_test import Mock, must_equal, var
import os 


def func_c(*args, **kwargs):

    return sum(args) + sum(kwargs.values())



def ___test_mocked_function(*args, **kwargs):
    return sum(args) + sum(kwargs.values())


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
