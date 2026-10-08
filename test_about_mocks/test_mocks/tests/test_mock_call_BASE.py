from tini_test.mock import Mock
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test


def add_args_function(*args, k_val_1: int = 0, k_val_2: int = 0) -> int:
    return sum(args) + k_val_1 + k_val_2

def add_args_function1(*args, k_val_1: int = 0, k_val_2: int = 0) -> int:
    return sum(args) + k_val_1 + k_val_2

def add_args_function2(*args, k_val_1: int = 0, k_val_2: int = 0) -> int:
    return sum(args) + k_val_1 + k_val_2


@Mock.mock(add_args_function, kwargs={'k_val_1': 10, 'k_val_2': 20})
@Test.case
def test_mock_passing_keywords():
    must_equal(30, add_args_function(k_val_1=1_000, k_val_2=1_000))
    print('works')



@Mock.mock(add_args_function1, args=(1, 2))
@Test.case
def test_passing_positional_arguments_to_add_args_function():
    must_equal(3, add_args_function1(1_000, 1_000, k_val_1=1_000, k_val_2=1_000))
    print('works')


@Mock.mock(add_args_function2, args=(1, 2), kwargs={'k_val_1': 10, 'k_val_2': 20})
@Test.case
def test_passing_both_positional_and_keyword_arguments_to_add_args_function():
    must_equal(1+2+10+20, add_args_function2(1_000, 1_000, k_val_1=1_000, k_val_2=1_000))
    print('works')



@Mock.mock(mock=add_args_function, kwargs={'k_val_1': 10, 'k_val_2': 20})
@Test.case
def test_positional_mock_passing_keywords():
    must_equal(30, add_args_function(k_val_1=1_000, k_val_2=1_000))
    print('works')



@Mock.mock(mock=add_args_function1, args=(1, 2))
@Test.case
def test_positional_mock_passing_positional_arguments_to_add_args_function():
    must_equal(3, add_args_function1(1_000, 1_000, k_val_1=1_000, k_val_2=1_000))
    print('works')


@Mock.mock(mock=add_args_function2, args=(1, 2), kwargs={'k_val_1': 10, 'k_val_2': 20})
@Test.case
def test_positional_mock_passing_both_positional_and_keyword_arguments_to_add_args_function():
    must_equal(1+2+10+20, add_args_function2(1_000, 1_000, k_val_1=1_000, k_val_2=1_000))
    print('works')
