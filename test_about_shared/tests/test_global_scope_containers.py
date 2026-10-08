
from tini_test.context_managers import WillRaise
from tini_test.misc.exceptions import SharedVarDoesNotExistInThisContext
from tini_test.must_equals import must_equal
from tini_test.shared import NotInitialized, Shared, var
from tini_test.test_utils import Test

# def in_scope_var(arg=var.int):
#     print(arg)
#     kappa = arg
#     return arg

# @Test.case
# @Shared(var.int, var.local)
# def test_default_param_value_on_var_in_scope():
#     ...




####################################

# @Test.case
# @Mock.mock(x := lambda arg1: arg1, returns=(var.int,))
# @Shared(var.int)
# def test_pass_var_on_return():
#     print('VAR INT =', var.int)
#     var.int = 123

#     must_equal(123, var.int)

#     print('RES =', x(var.int))
#     must_equal((NotInitialized,), x(var.int))



####################################


# def mocked_function_call_with_var(*args, var_a, **kwargs):

#     var.int, *_ = args

#     var.klass = MyNewClass
#     var.callable = lambda: 111
    
#     var.none = 'X'

#     return args, var_a, kwargs

# @Test.case                                                          #XXX
# @Mock.mock(mocked_function_call_with_var, args=(var.int,), kwargs={'var_a': var.klass, 
#                                                                    'klass': var.klass,
#                                                                    'callable': var.callable,
#                                                                    'none': var.none,}) # var on args TODO
# @Shared(var.int, var.klass, var.callable, var.none)
# def test_integration_mock_call_with_var():
#     var.int = 123
#     var.klass = type('MyClass', (), {})
#     var.callable = lambda: 100
#     var.none = None

#     args, var_a, kwargs = mocked_function_call_with_var(var_a=var.int)

#     must_equal(MyNewClass, var.klass)
#     must_equal(111, var.callable())
#     must_equal(46, var.int)
#     must_equal('X', var.none)

####################################
