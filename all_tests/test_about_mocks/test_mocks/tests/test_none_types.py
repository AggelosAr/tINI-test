from tini_test import Mock, Test, must_equal


def func_d(arg1, arg2, k_val_1=None, k_val_2=None):
    return (arg1 or 0) + (arg2 or 0) + (k_val_1 or 0) + (k_val_2 or 0)

@Mock.mock(func_d, args=(None, 100))
@Test.case()
def test_mock_none_in_args():
    print('works')
    must_equal(100, func_d(None, 999))


@Mock.mock(func_d, args=(1, None, ), kwargs={'k_val_1': None, 'k_val_2': 100})
@Test.case()
def test_mock_none_in_kwargs():
    print('works')
    must_equal(101, func_d(None))


@Mock.mock(func_d, returns=None)
@Test.case()
def test_mock_none_in_returns():
    print('works')
    must_equal(None, func_d(100, 1, k_val_1=100, k_val_2=100))



@Mock.mock(func_d, args=(None, None))
@Test.case()
def full_none_in_args():
    print('works')
    must_equal(0, func_d(100, 1, k_val_1=100, k_val_2=100))




class A:
    def __init__(self, value):
        self.value = value

def object_func(arg1, arg2=A(11)):
    return (arg1 or 0) + (arg2.value or 0)


@Mock.mock(object_func, args=(None, ), )
@Test.case()
def test_mock_none_in_object_func():
    print('works')
    must_equal(11, object_func(None))




