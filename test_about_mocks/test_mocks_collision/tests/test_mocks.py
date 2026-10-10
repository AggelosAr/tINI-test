from test_about_mocks.test_mocks.tests.test_imports import (add_args_function,
                                                            f1, f2)
from tini_test import Mock, Test, WillRaise, must_equal
from tini_test.misc.exceptions import ExpectedWasDifferentFromActual


@Mock.mock
@Test.case
def test_mock_decorator_order_M_T():
    print('works')



@Test.case
@Mock.mock
def test_mock_decorator_order_T_M():
    with WillRaise(ZeroDivisionError):
        must_equal(1, 1)
        print('works')
        1/0



@Mock.mock()
@Test.case()
def test_mock_decorator_order_M_T_pass_parentheses():
    with WillRaise(ZeroDivisionError):
        must_equal(1, 1)
        print('works')
        1/0

 
@Test.case()
@Mock.mock()
def test_mock_decorator_order_T_M_pass_parentheses():
    with WillRaise(ZeroDivisionError):
        must_equal(1, 1)
        print('works')
        1/0




@Mock.mock()
@Mock.mock
@Mock.mock
@Mock.mock()
@Test.case(f1, f2)
@Mock.mock
@Mock.mock()
@Mock.mock
@Mock.mock(add_args_function, args=((),))
@Mock.mock
def test_mock_decorator_orders_and_skips():
    with WillRaise(ZeroDivisionError):
        must_equal(1, 1)
        print('works')
        1/0



@Mock.mock(add_args_function, returns=1_000)
@Test.case
def test_mock_will_not_call_function_on_single_nested_calls():
    must_equal(1_000, add_args_function(1, k_val_1=1, k_val_2=1))
    print('works')



@Mock.mock(add_args_function, returns=[1_000])
@Test.case
def test_mock_will_return_correct_value():
    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(1_000, add_args_function(1, k_val_1=1, k_val_2=1))

    must_equal('''
ITEM: type mismatch
expected: <class 'int'>
actual:   <class 'list'>
[EOD]''', str(context.exception))
    print('works')



@Mock.mock(add_args_function, args=(1, 2, 3, 4, 5, 6, 7))
@Test.case
def test_mock_passing_arguments_to_add_args_function():
    must_equal(1 + 2 + 3 + 4 + 5 + 6 + 7, add_args_function(1_000, 
                                                            1_000, 
                                                            1_000, 
                                                            1_000, 
                                                            1_000, 
                                                            1_000, 
                                                            1_000))
    print('works')


@Mock.mock(add_args_function, kwargs={'k_val_1': 10, 'k_val_2': 20})
@Test.case
def test_mock_passing_keywords_to_add_args_function():
    must_equal(30, add_args_function(k_val_1=1_000, k_val_2=1_000))
    print('works')



@Mock.mock(add_args_function, args=(1, 2), kwargs={'k_val_1': 10, 'k_val_2': 20})
@Test.case
def test_passing_both_positional_and_keyword_arguments_to_add_args_function():
    must_equal(1+2+10+20, add_args_function(1_000, 1_000, k_val_1=1_000, k_val_2=1_000))
    print('works')



_D = 1_000
def _setup():
    global _D
    must_equal(1_000, _D)
    _D += add_args_function(1_000_000, 
                            1_000_000, 
                            1_000_000, 
                            k_val_1=1_000_000, 
                            k_val_2=1_000_000)
    must_equal(1_000 + 1_000 + 1_000, _D)


def _cleanup():
    global _D
    must_equal(1_000 + 1_000 + 1_000 + 1_000 + 1_000, _D)


@Mock.mock(add_args_function, args=(1_000,), kwargs={'k_val_1': 1_000})
@Test.case(
        setup=_setup,
        cleanup=_cleanup
)
def test_mock_with_setup_and_cleanup():
    must_equal(1_000 + 1_000, x := add_args_function(1_000_000, 
                                                     1_000_000, 
                                                     1_000_000, 
                                                     k_val_1=1_000_000, 
                                                     k_val_2=1_000_000))
    global _D
    must_equal(1_000 + 1_000 + 1_000, _D)
    _D += x
    print('works')



_X = 1_000
def _setup():
    global _X
    must_equal(1_000, _X)
    _X += add_args_function(1_000_000, 
                            1_000_000, 
                            1_000_000, 
                            k_val_1=1_000_000, 
                            k_val_2=1_000_000)
    must_equal(1_000 + 1_000 + 1_000, _X)


def _cleanup():
    global _X
    must_equal(1_000 + 1_000 + 1_000 + 1_000 + 1_000, _X)


@Mock.mock(add_args_function, args=(1_000,), kwargs={'k_val_1': 1_000})
@Test.case(
        setup=_setup,
        cleanup=_cleanup
)
def test_mock_with_setup_and_cleanup_reverse_decorator_order():
    must_equal(1_000 + 1_000, x := add_args_function(1_000_000, 
                                                     1_000_000, 
                                                     1_000_000, 
                                                     k_val_1=1_000_000, 
                                                     k_val_2=1_000_000))
    global _X
    must_equal(1_000 + 1_000 + 1_000, _X)
    _X += x
    print('works')




def f1(x, a, b):
    return x + a + b

def f2(x, c, d):
    return x + c + d

def f3(x, f, g):
    return x + f + g


@Mock.mock(f1, args=(1,), kwargs={'a': 8, 'b': 5})
@Mock.mock(f2, args=(9,), kwargs={'c': 2, 'd': 7})
@Mock.mock(f3, args=(4,), kwargs={'f': 6, 'g': 3})
@Test.case()
def test_multiple_mocks_with_args():
    must_equal(1 + 8 + 5, f1(1_000, a=8_000, b=5_000))
    must_equal(9 + 2 + 7, f2(9_000, c=2_000, d=7_000))
    must_equal(4 + 6 + 3, f3(4_000, f=6_000, g=3_000))

    must_equal(1 + 8 + 5 + 9 + 2 + 7 + 4 + 6 + 3, 
               f1(1_000, a=8_000, b=5_000) + 
               f2(9_000, c=2_000, d=7_000) + 
               f3(4_000, f=6_000, g=3_000))
    print('works')



@Test.case()
@Mock.mock(f1, args=(1,), kwargs={'a': 8, 'b': 5})
@Mock.mock(f2, args=(9,), kwargs={'c': 2, 'd': 7})
@Mock.mock(f3, args=(4,), kwargs={'f': 6, 'g': 3})
def test_multiple_mocks_with_args_ord():
    must_equal(1 + 8 + 5, f1(1_000, a=8_000, b=5_000))
    must_equal(9 + 2 + 7, f2(9_000, c=2_000, d=7_000))
    must_equal(4 + 6 + 3, f3(4_000, f=6_000, g=3_000))

    must_equal(1 + 8 + 5 + 9 + 2 + 7 + 4 + 6 + 3, 
               f1(1_000, a=8_000, b=5_000) + 
               f2(9_000, c=2_000, d=7_000) + 
               f3(4_000, f=6_000, g=3_000))
    print('works')



@Mock.mock(f1, args=(1,), kwargs={'a': 8, 'b': 5})
@Test.case()
@Mock.mock(f2, args=(9,), kwargs={'c': 2, 'd': 7})
@Mock.mock(f3, args=(4,), kwargs={'f': 6, 'g': 3})
def test_multiple_mocks_with_args_ord_2():
    must_equal(1 + 8 + 5, f1(1_000, a=8_000, b=5_000))
    must_equal(9 + 2 + 7, f2(9_000, c=2_000, d=7_000))
    must_equal(4 + 6 + 3, f3(4_000, f=6_000, g=3_000))

    must_equal(1 + 8 + 5 + 9 + 2 + 7 + 4 + 6 + 3, 
               f1(1_000, a=8_000, b=5_000) + 
               f2(9_000, c=2_000, d=7_000) + 
               f3(4_000, f=6_000, g=3_000))
    print('works')



@Mock.mock(f1, args=(1,), kwargs={'a': 8, 'b': 5})
@Mock.mock(f2, args=(9,), kwargs={'c': 2, 'd': 7})
@Test.case
@Mock.mock(f3, args=(4,), kwargs={'f': 6, 'g': 3})
def test_multiple_mocks_with_args_ord_3():
    must_equal(1 + 8 + 5, f1(1_000, a=8_000, b=5_000))
    must_equal(9 + 2 + 7, f2(9_000, c=2_000, d=7_000))
    must_equal(4 + 6 + 3, f3(4_000, f=6_000, g=3_000))

    must_equal(1 + 8 + 5 + 9 + 2 + 7 + 4 + 6 + 3, 
               f1(1_000, a=8_000, b=5_000) + 
               f2(9_000, c=2_000, d=7_000) + 
               f3(4_000, f=6_000, g=3_000))
    print('works')


@Mock.mock(f1, returns=10)
@Mock.mock(f2, returns=20)
@Mock.mock(f3, returns=30)
@Test.case()
def test_multiple_mocks_with_returns():
    must_equal(10, f1(1_000, a=8_000, b=5_000))
    must_equal(20, f2(9_000, c=2_000, d=7_000))
    must_equal(30, f3(4_000, f=6_000, g=3_000))

    must_equal(10 + 20 + 30, 
                f1(1_000, a=8_000, b=5_000) + 
                f2(9_000, c=2_000, d=7_000) + 
                f3(4_000, f=6_000, g=3_000))
    print('works')

