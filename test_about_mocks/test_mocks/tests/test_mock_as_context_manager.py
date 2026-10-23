from tini_test import Mock, Test, Shared, var, must_equal, Isolate, WillRaise
from tini_test.misc.exceptions import MockClassDefinitionError


class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add_more(self, z):
        return self.x + self.y + z


class MyClass2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    

@Isolate
@Test.case()
def test_mocking_as_context_manager():

    with Mock.mocking(MyClass, args=(1, 2)):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    with Mock.mocking(MyClass, args=(1,), kwargs={'y': 2}):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    with Mock.mocking(MyClass, kwargs={'x': 1, 'y': 2}):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    with Mock.mocking(MyClass.add_more, args=(MyClass, 1_000,)):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass.add_more, args=(MyClass,), kwargs={'z': 1_000}):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass.add_more, kwargs={'self': MyClass, 'z': 1_000}):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass, args=(3, 4)):
        with Mock.mocking(MyClass.add_more, args=(MyClass, 1_000_000,)):
            instance = MyClass('?', '?')
            must_equal(3, instance.x)
            must_equal(4, instance.y)
            must_equal(3 + 4 + 1_000_000, instance.add_more('?'))
            print('works')

    print('works')


# Validate low level mocking overrides higher level mocking

# TODO add test for nesting mockings

@Isolate
@Mock.mock(MyClass, args=('xyz', 'xyz'))
@Mock.mock(MyClass2, args=('xyz', 'xyz'))
@Mock.mock(MyClass.add_more, args=('xyz', 'xyz',))
@Test.case()
def test_mocking_order():

    with Mock.mocking(MyClass, args=(1, 2)):
        instance = MyClass('?', '?')
        print('instance x:', instance.x)
        print('instance y:', instance.y)

        must_equal(1, instance.x)
        must_equal(2, instance.y)

        # Validate wrong items are not overridden by the low-level mock
        instance2 = MyClass2('?', '?')
        must_equal('xyz', instance2.x)
        must_equal('xyz', instance2.y)

    with Mock.mocking(MyClass, args=(1,), kwargs={'y': 2}):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    with Mock.mocking(MyClass, kwargs={'x': 1, 'y': 2}):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    with Mock.mocking(MyClass.add_more, args=(MyClass, 1_000,)):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass.add_more, args=(MyClass,), kwargs={'z': 1_000}):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass.add_more, kwargs={'self': MyClass, 'z': 1_000}):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass, args=(3, 4)):
        with Mock.mocking(MyClass.add_more, args=(MyClass, 1_000_000,)):
            instance = MyClass('?', '?')
            must_equal(3, instance.x)
            must_equal(4, instance.y)
            must_equal(3 + 4 + 1_000_000, instance.add_more('?'))
            print('works')

    print('works')


# Test shared integration


@Isolate
@Test.case
@Shared(var.a, var.b, var.c, var.d)
def test_mocking_as_context_manager_with_shared_integration():

    var.a, var.b = 1, 2
    
    with Mock.mocking(MyClass, args=(var.a, var.b)):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    with Mock.mocking(MyClass, args=(var.a,), kwargs={'y': var.b}):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    with Mock.mocking(MyClass, kwargs={'x': var.a, 'y': var.b}):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)


    var.c = 1_000

    with Mock.mocking(MyClass.add_more, args=(MyClass, var.c,)):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass.add_more, args=(MyClass,), kwargs={'z': var.c}):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass.add_more, kwargs={'self': MyClass, 'z': var.c}):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))


    var.a, var.b = 3, 4
    var.c = 1_000_000
    var.d = MyClass

    with Mock.mocking(MyClass, args=(var.a, var.b)):
        with Mock.mocking(MyClass.add_more, args=(var.d, var.c,)):
            instance = MyClass('?', '?')
            must_equal(3, instance.x)
            must_equal(4, instance.y)
            must_equal(3 + 4 + 1_000_000, instance.add_more('?'))
            print('works')

    print('works')



# Test mocking exceptions
# TODO maybe add all the exceptions here? Since now we can...
@Isolate
@Test.case()
def test_exceptions():

    def func_e(arg1, arg2, k_val_1=1000, k_val_2=2000):
        return (arg1 or 0) + (arg2 or 0) + (k_val_1 or 0) + (k_val_2 or 0)

    # XXX 
    with WillRaise(TypeError) as context:
        with Mock.mocking(func_e, args=(None, None, 100, 100), kwargs={'k_val_2': 100}):
            func_e('?')

    must_equal("multiple values for argument 'k_val_2'", str(context.exception))
  
    class MyClass:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def add(self):
            return self.x + self.y

    with WillRaise(MockClassDefinitionError) as context:
        with Mock.mocking(MyClass, returns=MyClass(100, 100)):
            MyClass('?')

    must_equal('Mock class only accepts initialization arguments.', str(context.exception))

