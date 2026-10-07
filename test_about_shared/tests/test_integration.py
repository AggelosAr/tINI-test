from tini_test.mock import Mock
from tini_test.must_equals import must_equal
from tini_test.shared import NotInitialized, Shared, SharedVar, var
from tini_test.test_utils import Test

# TODO Also test import on 1 and 2 levels of nesting


def simple_function(use):
    if use:
        var.int = 123
    return var.int

@Test.case
@Shared(var.int)
def test_function_returns_var():
    must_equal(NotInitialized, simple_function(use=False))
    must_equal(123, simple_function(use=True))
    must_equal(123, var.int)



def simple_function_with_default(arg=var.int):
    return arg

@Test.case
@Shared(var.int)
def test_default_param_value_on_var():
    res = simple_function_with_default()
    print('res =', res)
    print('res value=', res.value)
    print('res value value=', res.value.value) # Works BUT !! TOOD for some reason not expanded automatigally
    must_equal(NotInitialized, res)
    var.int = 123
    must_equal(123, simple_function_with_default())



# This should error when calling the function since it is not in scope
def simple_function_with_default_exception(arg=var.intX):
    return arg

@Test.case
@Shared(var.int)
def test_default_param_value_on_var_exception():
    res = simple_function_with_default()
    print('res =', res)
    print('res value=', res.value)
    print('res value value=', res.value.value)
    must_equal(NotInitialized, res)
   


####################################

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

@Test.case
@Mock.mock(x := lambda arg1: arg1, returns=(var.int,))  # returns var todo TODO 
@Shared(var.int)
def test_pass_var_on_return():
    raise
    var.int = 123

    must_equal(123, var.int)

    print('x(var.int) =', x(var.int))
    
    must_equal((123,), x(var.int))

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




####################################


def mocked_function_call_with_var(*args, var_a, **kwargs):

    var.int, *_ = args

    var.klass = MyNewClass
    var.callable = lambda: 111
    
    var.none = 'X'

    return args, var_a, kwargs

@Test.case                                                          #XXX
@Mock.mock(mocked_function_call_with_var, args=(var.int,), kwargs={'var_a': var.klass, 
                                                                   'klass': var.klass,
                                                                   'callable': var.callable,
                                                                   'none': var.none,}) # var on args TODO
@Shared(var.int, var.klass, var.callable, var.none)
def test_integration_mock_call_with_var():
    var.int = 123
    var.klass = type('MyClass', (), {})
    var.callable = lambda: 100
    var.none = None

    args, var_a, kwargs = mocked_function_call_with_var(var_a=var.int)

    must_equal(MyNewClass, var.klass)
    must_equal(111, var.callable())
    must_equal(46, var.int)
    must_equal('X', var.none)

####################################


