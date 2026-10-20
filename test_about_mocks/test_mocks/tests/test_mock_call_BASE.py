from dataclasses import dataclass

from tini_test import Mock, Test, must_equal


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



class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self):
        return self.x + self.y

    def add_more(self, z):
        return self.x + self.y + z


@Mock.mock(MyClass, args=(1, 2))
@Test.case()
def test_mocking_my_class():
    instance = MyClass(10, 20)
    must_equal(1, instance.x)
    must_equal(2, instance.y)
    must_equal(1 + 2, instance.add())
    print('works')

    instance = MyClass()
    must_equal(1, instance.x)
    must_equal(2, instance.y)
    must_equal(1 + 2, instance.add())
    print('works')



@dataclass
class MyDataClass:

    x: int
    y: int

    def add(self):
        return self.x + self.y

    
@Mock.mock(MyDataClass, args=(1, 2))
@Mock.mock(MyDataClass.add, returns=1_000)
@Test.case()
def test_mocking_my_data_class_and_method_returns_mocked_value():
    instance = MyDataClass(10, 20)
    must_equal(1, instance.x)
    must_equal(2, instance.y)
    must_equal(1_000, instance.add())
    print('works')

    instance = MyDataClass()
    must_equal(1, instance.x)
    must_equal(2, instance.y)
    must_equal(1_000, instance.add())
    print('works')



@Mock.mock(MyClass, args=(1, 2))
@Mock.mock(MyClass.add_more, args=(MyClass, 1_000,))
@Test.case()
def test_mocking_my_class_method_args_mocked_value():
    instance = MyClass(10, 20)
   
    must_equal(1 + 2 + 1_000, instance.add_more(1_000_000))
    print('works')

    instance = MyClass()
    must_equal(1 + 2 + 1_000, instance.add_more(1_000_000))
    print('works')


# TODO add test for classmethod and staticmethod ?