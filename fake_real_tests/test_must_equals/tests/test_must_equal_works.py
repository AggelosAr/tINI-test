from small_test.context_manager import WillRaise
from small_test.misc.exceptions import (ComperatorIsNotValid,
                                        ComperatorWasNotProvided,
                                        ExpectedWasDifferentFromActual)
from small_test.must_equals import must_equal
from small_test.test_utils import Test




@Test.case
def test_must_equal_receives_unknwon_object_no_comperator_provided() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = 10

    with WillRaise(ComperatorWasNotProvided) as context:
        must_equal(A(10), A(20))

    must_equal('Unknown type encountered and a comperator was not provided.', str(context.exception))



@Test.case
def test_comperator_works_on_unknown_objects_in_containers_if_is_provided_and_returns_false() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

    
    def custom_comperator(a: A, b: A):
        return a.a == b.a
 
    obj1 = [A(a=10)]
    obj2 = [A(a=20)]

    with WillRaise(ExpectedWasDifferentFromActual):
        must_equal(obj1, obj2, comperator=custom_comperator)



@Test.case
def test_comperator_works_on_unknown_objects_in_containers_if_is_provided_and_returns_true() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

    def custom_comperator(a: A, b: A):
        return a.a == b.a
 
    obj1 = [A(a=10)]
    obj2 = [A(a=10)]

    must_equal(obj1, obj2, comperator=custom_comperator)



@Test.case
def test_must_equals_auto_discovers_eq_and_returns_false() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

        def __eq__(self, other: object) -> bool:

            if not isinstance(other, A):
                return NotImplemented
            
            return self.a == other.a
 
    obj1 = [A(a=10)]
    obj2 = [A(a=20)]

    with WillRaise(ExpectedWasDifferentFromActual):
        must_equal(obj1, obj2)



@Test.case
def test_must_equals_auto_discovers_eq_and_returns_true() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

        def __eq__(self, other: object) -> bool:

            if not isinstance(other, A):
                return NotImplemented
            
            return self.a == other.a
 
    obj1 = [A(a=10)]
    obj2 = [A(a=10)]

    must_equal(obj1, obj2)



@Test.case
def test_comperator_works_on_unknown_objects_in_containers_case_pass() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

        def __eq__(self, obj):
            return self.a == obj.a
    
    must_equal([A(10)], [A(10)], comperator=A.__eq__)



@Test.case
def test_comperator_works_on_unknown_objects_in_containers_case_fail() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

        def __eq__(self, obj):
            return self.a == obj.a
    
    with WillRaise(ExpectedWasDifferentFromActual):
        must_equal([A(10)], [A(20)], comperator=A.__eq__)
