from tini_test.must_equals import must_equal
from tini_test.shared import NotInitialized, Shared, SharedVar, var
from tini_test.test_utils import Test

# class

@Shared(var.callable)
@Test.case
def test_callable():
    var.callable = lambda: 100
    must_equal(100, var.callable())


@Shared(var.empty)
@Test.case
def test_empty():
    var.empty = None
    must_equal(None, var.empty)


@Shared(var.klass)
@Test.case
def test_class():

    class MyClass:
        pass

    var.klass = MyClass
    must_equal(MyClass, var.klass)


@Shared(var.klass, var.callable, var.int)
@Test.case
def test_class_with_callable_with_int():

    class MyClass:
        pass

    var.klass = MyClass
    must_equal(NotInitialized, var.callable)
    must_equal(NotInitialized, var.int)

    var.callable = lambda: 100
    must_equal(NotInitialized, var.int)

    var.int = 42

    must_equal(MyClass, var.klass)
    must_equal(100, var.callable())
    must_equal(42, var.int)
