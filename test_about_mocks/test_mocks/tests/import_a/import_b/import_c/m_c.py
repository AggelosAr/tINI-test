from tini_test import Mock, must_equal


def func_c(*args, **kwargs):

    return sum(args) + sum(kwargs.values())



def ___test_mocked_function(*args, **kwargs):
    return sum(args) + sum(kwargs.values())


def ___test_mocking_in_outside_function(*args, **kwargs):
    with Mock.mocking(___test_mocked_function, args=(5, 5), kwargs={'k_val_1': 5}):
        result = ___test_mocked_function('?')
    must_equal(15, result)
    return result