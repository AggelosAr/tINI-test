from tini_test.context_managers import WillRaise
from tini_test.misc.exceptions import SharedVarDoesNotExistInThisContext
from tini_test.must_equals import must_equal
from tini_test.shared import NotInitialized, Shared, var
from tini_test.test_utils import Test


def simple_function(use):
    if use:
        var.int = 123
    return var.int

@Test.case
@Shared(var.int)
def test_function_returns_var():
    must_equal(NotInitialized, simple_function(use=False))
    must_equal(NotInitialized, var.int)
    must_equal(123, simple_function(use=True))
    must_equal(123, var.int)



def side_effect_function(arg):
    var.int = arg
    return var.int


@Test.case
@Shared(var.int)
def test_side_effects():
    must_equal(NotInitialized, var.int)
    side_effect_function(456)
    must_equal(456, var.int)




@Test.case
@Shared(var.int, var.b)
def test_in_scope_func_def():

    def in_scope_function(arg=var.int):
        return arg

    must_equal(NotInitialized, in_scope_function())


    var.b = 72
    def in_scope_function(arg=var.b):
            return arg
    
    must_equal(72, in_scope_function())



@Test.case
@Shared(var.int, var.b)
def test_raises():

    with WillRaise(SharedVarDoesNotExistInThisContext) as context:

        def in_scope_function(arg=var.x):
            return arg

    msg = 'Shared variable < x > does not exist in this context. For test < test_raises >'
    print(str(context.exception))
    must_equal(msg, str(context.exception))


    def in_scope_function(arg):
        var.x = 100
        return arg

    with WillRaise(SharedVarDoesNotExistInThisContext) as context:
        in_scope_function(10)
    msg = 'Shared variable < x > does not exist in this context. For test < test_raises >'
    print(str(context.exception))
    must_equal(msg, str(context.exception))



