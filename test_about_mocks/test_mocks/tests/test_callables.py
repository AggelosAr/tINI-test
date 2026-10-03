from typing import Callable, Optional

from tini_test.mock import Mock
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test

c_r = lambda: 999
c_x = lambda: 1000

def func_g():
    return c_x

@Mock.mock(func_g, returns=c_r)
@Test.case()
def test_mock_callable_in_returns():
    print('works')
    must_equal(c_r, func_g())
    result = func_g()()
    must_equal(999, result)



def func_e(arg1: Callable, arg2, k_val_1: Optional[Callable]=None, k_val_2=None):
    return (arg1() or 0) + arg2 + (k_val_1() if k_val_1 else 0) + (k_val_2 or 0)

def func_f():
    return 100



@Mock.mock(func_e, args=(lambda: 999, 1), kwargs={'k_val_1': func_f, 'k_val_2': None})
@Test.case()
def test_mock_anon_callable_none_in_args_kwargs():
    print('works')
    must_equal(999 + 1 + 100, func_e(func_f, 1, k_val_1=func_f, k_val_2=100))


@Mock.mock(func_e, args=(func_f, 1), kwargs={'k_val_1': func_f, 'k_val_2': None})
@Test.case()
def test_mock_callable_none_in_args_kwargs():
    print('works')
    must_equal(100 + 1 + 100, func_e(lambda: 999, 1, k_val_1=lambda: 999, k_val_2=100))





