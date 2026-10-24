import traceback as tb

from tini_test import Mock, Test, WillRaise, must_equal

# Validate proxy view names. 


class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def my_method(self): ...


@Test.case
@Mock.mock(MyClass, args=('xyz', 'xyz', 'a'))
def test_mock_my_class_init_proxy_name():

    with WillRaise(TypeError) as context:
        MyClass('xyz', 'xyz')

    must_equal('too many positional arguments', str(context.exception))

    print(''.join(tb.format_tb(context.exc_traceback)))

    must_equal(True, '_proxy_MyClass___init___' in ''.join(tb.format_tb(context.exc_traceback)))



# TODO maybe update how this is handled.
@Test.case
@Mock.mock(MyClass.my_method, args=(MyClass, 'xyz', 'xyz', 'a'))
def test_mock_my_class_method_proxy_name():

    with WillRaise(TypeError) as context:
        MyClass('xyz', 'xyz').my_method()

    must_equal('too many positional arguments', str(context.exception))
    print(''.join(tb.format_tb(context.exc_traceback)))
    must_equal(True, '_proxy_my_method_' in ''.join(tb.format_tb(context.exc_traceback)))


def my_function(): ...

@Test.case
@Mock.mock(my_function, args=('xyz', 'xyz', 'a'))
def test_mock_my_function_proxy_name():

    with WillRaise(TypeError) as context:
        my_function('xyz', 'xyz')

    # TODO this prints in the start we fail to collect it 
    # import traceback
    # traceback.print_tb(context.exception.__traceback__)

    traceback = context.exc_traceback
    must_equal('too many positional arguments', str(context.exception))
    must_equal(True, '_proxy_my_function_' in ''.join(tb.format_tb(traceback)))



