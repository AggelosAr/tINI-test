from dataclasses import dataclass

from tini_test.must_equals import must_equal
from tini_test.shared import NotInitialized, Shared, var
from tini_test.test_utils import Test


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



@Shared(var.a, var.b, var.c, var.d, var.e)
@Test.case
def test_nested_structures_dict():

    var.a = {'key': {'subkey': 42}}
    must_equal({'key': {'subkey': 42}}, var.a)
    print('--> LH Assignment good\n')


    a = {'key': {'subkey': var.b}}
    must_equal(NotInitialized, a['key']['subkey'])
    print('--> Creating nested structure with NotInitialized value\n')


    var.b = 42
    must_equal(NotInitialized, a['key']['subkey'])
    print("--> Updated var.b and won't be reflected in nested structure since it is a view\n")


    var.c = 42
    b = {'key': {'subkey': var.c}}
    must_equal(42, b['key']['subkey'])
    b['key']['subkey'] = 66
    must_equal(66, b['key']['subkey'])
    must_equal(42, var.c)
    print('--> RH Access after var.c assignment good\n')


    var.d = 'key'
    somes = {var.d: {'subkey': var.c}}
    must_equal(42, somes[var.d]['subkey'])
    print('--> Using var as key good\n')

    var.d = NotInitialized
    must_equal(NotInitialized, var.d)
    print('--> Reset var.d to NotInitialized\n')


    somes = {var.e: {'subkey': var.c}}
    must_equal(NotInitialized, list(somes.keys())[0])
    print('--> Using NotInitialized as key good\n')


    must_equal(var.c, somes[var.e]['subkey'])
    print('--> Accessing nested structure with NotInitialized key and value good\n')



@Shared(var.a, var.b, var.c, var.d)
@Test.case
def test_nested_structures_list():
    var.a = [1, 2, 3]
    must_equal([1, 2, 3], var.a)
    print('--> LH Assignment good\n')


    a = [1, 2, var.b]
    must_equal(NotInitialized, a[2])
    print('--> Creating nested structure with NotInitialized value\n')


    var.b = 42
    must_equal(NotInitialized, a[2])
    print("--> Updated var.b and won't be reflected in nested structure since it is a view\n")


    var.c = 42
    b = [1, 2, var.c]
    must_equal(42, b[2])
    b[2] = 66
    must_equal(66, b[2])
    must_equal(42, var.c)
    print('--> RH Access after var.c assignment good\n')


    var.d = 0
    somes = [var.c]
    must_equal(42, somes[var.d])
    print('--> Using var as key good\n')

    var.d = NotInitialized
    must_equal(NotInitialized, var.d)
    print('--> Reset var.d to NotInitialized\n')



@Test.case()
@Shared(var.a, var.b, var.c, var.d, var.e, var.f)
def test_class_attrs():

    comp = lambda a, b: a.a==b.a and a.b==b.b and a.c==b.c

    class MyClass:
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

    var.a = MyClass(var.b, var.c, var.d)
    must_equal(MyClass(var.b, var.c, var.d), var.a, comp)
    must_equal(var.b, var.a.a)
    must_equal(var.c, var.a.b)
    must_equal(var.d, var.a.c)
    print('--> Class attribute assignment good\n')

    @dataclass
    class MyDataClass:
        a: any
        b: any
        c: any

    var.a = MyDataClass(var.b, var.c, var.d)
    must_equal(MyDataClass(var.b, var.c, var.d), var.a, comp)
    must_equal(var.b, var.a.a)
    must_equal(var.c, var.a.b)
    must_equal(var.d, var.a.c)
    print('--> Data class attribute assignment good\n')


    # This works cause it is in scope.
    class ClassWithAttrs:
        def __init__(self, a, b=var.f):
            self.a = a
            self.b = b
            self.c = var.e

    instance = ClassWithAttrs(var.a, )
    must_equal(var.a, instance.a)
    must_equal(NotInitialized, instance.b)
    must_equal(NotInitialized, instance.c)
    print('--> Class with attributes including shared var.e var.f good\n')
