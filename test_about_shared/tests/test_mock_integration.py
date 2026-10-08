from tini_test.mock import Mock
from tini_test.must_equals import must_equal
from tini_test.shared import Shared, var
from tini_test.test_utils import Test


class MyNewClass:
    pass


def mocked_function_return(*args, var_a, **kwargs):

    var.klass = MyNewClass
    var.callable = lambda: 111
    var.int = 46
    var.none = 'X'
    return args, var_a, kwargs



@Test.case
@Mock.mock(mocked_function_return, returns=(123,))
@Shared(var.int, var.klass, var.callable, var.none)
def test_integration_mock_return():
    class MyClass:
        pass
    var.klass = MyClass
    var.callable = lambda: 100
    var.int = 42
    var.none = None

    res = mocked_function_return(var_a=var.int)
    must_equal((123, ), res)

    must_equal(MyClass, var.klass)
    must_equal(100, var.callable())
    must_equal(42, var.int)
    must_equal(None, var.none)


####################################


def mocked_function_call(*args, var_a, **kwargs):

    var.klass = MyNewClass
    var.callable = lambda: 111
    var.int = 46
    var.none = 'X'

    return args, var_a, kwargs


@Test.case
@Mock.mock(mocked_function_call, args=(123,), kwargs={'var_a': 123})
@Shared(var.int, var.klass, var.callable, var.none)
def test_integration_mock_call():
    var.int = 123
    var.klass = type('MyClass', (), {})
    var.callable = lambda: 100
    var.none = None

    args, var_a, kwargs = mocked_function_call(var_a=var.int)

    must_equal(MyNewClass, var.klass)
    must_equal(111, var.callable())
    must_equal(46, var.int)
    must_equal('X', var.none)

