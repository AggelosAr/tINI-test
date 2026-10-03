from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
    func_c
from test_about_mocks.test_mocks.tests.import_a.m_a import func_a
from tini_test.mock import Mock
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test


def add_args_function(*args, k_val_1: int = 0, k_val_2: int = 0) -> int:
    return sum(args) + k_val_1 + k_val_2



def f1():
    print('f1 called')



def f2():
    print('f2 called')



def value_to_sum(value):

    if isinstance(value, int):

        return value

    if isinstance(value, float):

        return value

    if isinstance(value, str):

        return int(value)

    if isinstance(value, list):

        return sum(value)

    if isinstance(value, dict):

        return sum(value.values())



def generated_function_16(a, b):
    print('generated_function_16')
    return value_to_sum(a) + value_to_sum(b)


def generated_function_17(a, b):
    print('generated_function_17')
    return value_to_sum(a) + value_to_sum(b)







# Test nesting imports
@Mock.mock(func_c, args=(1,), kwargs={'k_val_1': 1, 'k_val_2': 1})
@Test.case()
def test_mock_nested_call_args():
    print('works')
    must_equal(3 + 2, func_a(100, k_val_1=100, k_val_2=100))


@Mock.mock(func_c, returns=1000)
@Test.case()
def test_mock_nested_call_returns():
    print('works')
    must_equal(1000 + 2, func_a(100, k_val_1=100, k_val_2=100))
# Test nesting imports

