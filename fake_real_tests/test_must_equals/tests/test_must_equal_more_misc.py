from small_test.context_manager import WillRaise
from small_test.misc.exceptions import (ComperatorWasNotProvided,
                                        ExpectedWasDifferentFromActual)
from small_test.must_equals import must_equal
from small_test.test_utils import Test

# These are actual seperate cases ....

@Test.case
def test_must_equal_different_objects() -> None:

    obj1 = 1
    obj2 = 'a'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2)

    must_equal('''
ITEM: type mismatch
expected: <class 'int'>
actual:   <class 'str'>
''', str(context.exception))



@Test.case
def test_must_equal_different_objects_different_order() -> None:

    obj1 = 1
    obj2 = 'a'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2)

    must_equal('''
ITEM: type mismatch
expected: <class 'int'>
actual:   <class 'str'>
''', str(context.exception))



@Test.case
def test_must_equal_alien_object() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

 
    obj1 = A(11)
    obj2 = A(21)

    with WillRaise(ComperatorWasNotProvided) as context:
        must_equal(obj1, obj2)

    must_equal('Unknown type encountered and a comperator was not provided.', str(context.exception))



@Test.case
def test_must_equal_alien_object_different_order() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

    obj1 = A(21)
    obj2 = A(11)

    with WillRaise(ComperatorWasNotProvided) as context:
        must_equal(obj1, obj2)

    must_equal('Unknown type encountered and a comperator was not provided.', str(context.exception))


@Test.case
def test_must_equal_alien_object_with_eq() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

        def __eq__(self, other: object) -> bool:

            if not isinstance(other, A):
                return NotImplemented
            
            return self.a == other.a
        
    obj1 = A(11)
    obj2 = A(21)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2)

    must_equal('''
ITEM: <Object A at %s> != <Object A at %s>
''' % (hex(id(obj1)), hex(id(obj2)), ), str(context.exception))



@Test.case
def test_must_equal_alien_object_with_eq_different_order() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

        def __eq__(self, other: object) -> bool:

            if not isinstance(other, A):
                return NotImplemented
            
            return self.a == other.a
        
    obj1 = A(21)
    obj2 = A(11)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2)

    must_equal('''
ITEM: <Object A at %s> != <Object A at %s>
''' % (hex(id(obj1)), hex(id(obj2)), ), str(context.exception))



@Test.case
def test_must_equal_alien_object_with_cumtom_comp() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

    def custom_comperator(a: A, b: A):
        return a.a == b.a
        
    obj1 = A(11)
    obj2 = A(21)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2, comperator=custom_comperator)

    must_equal('''
ITEM: <Object A at %s> != <Object A at %s>
''' % (hex(id(obj1)), hex(id(obj2)), ), str(context.exception))



@Test.case
def test_must_equal_alien_object_with_cumtom_comp_different_order() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

    def custom_comperator(a: A, b: A):
        return a.a == b.a
    
    obj1 = A(21)
    obj2 = A(11)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2, comperator=custom_comperator)

    must_equal('''
ITEM: <Object A at %s> != <Object A at %s>
''' % (hex(id(obj1)), hex(id(obj2)), ), str(context.exception))



@Test.case
def test_must_equals_auto_discovers_eq_and_returns_false_format_case() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

        def __eq__(self, other: object) -> bool:

            if not isinstance(other, A):
                return NotImplemented
            
            return self.a == other.a
 
    obj1 = A(a=10)
    obj2 = A(a=20)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2)

    must_equal('''
ITEM: <Object A at %s> != <Object A at %s>
''' % (hex(id(obj1)), hex(id(obj2)), ), str(context.exception))



@Test.case
def test_must_equal_different_objects() -> None:

    expected = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    actual = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    must_equal('''
ITEM: <Object bytes at %s> != <Object bytes at %s>
''' % (hex(id(expected)), hex(id(actual)), ), str(context.exception))
