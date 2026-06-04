from typing import assert_never

from tini_test._internals._equals_engine import _must_equal
from tini_test.context_manager import WillRaise
from tini_test.must_equals import must_equal
from tini_test.test_suite import Test


@Test.case
def test_broken_test_case_one():
    print('test_broken_test_case_one')
    1/0
    assert_never()



@Test.case
def test_broken_test_case_two():
    print('test_broken_test_case_two')
    ok
    assert_never()



def setup_breaks():
    print('setup_breaks---->This should print and fail the test')
    1/0

@Test.case(setup=lambda: setup_breaks())
def test_setup_breaks():
    print('test_setup_breaks---->This should never print')
    assert_never()



def cleanup_breaks():
    print('cleanup_breaks---->This should print and fail the test')
    1/0

@Test.case(cleanup=lambda: cleanup_breaks())
def test_cleanup_breaks():
    print('test_cleanup_breaks---->This should print and then the clean up will divide by zero')



def _cleanup_breaks():
    print('_cleanup_breaks---->This should never print')
    assert_never()

@Test.case(setup=lambda: setup_breaks(), 
           cleanup=lambda: _cleanup_breaks())
def test_cleanup_breaks_test_and_break_down_wont_run():
    print('---->This should never print')
    assert_never()



@Test.case
def test_will_raise_fails_to_catch_exception() -> None:
    a = 0.1 + 0.2
    b = 0.3

    with WillRaise(ZeroDivisionError) as context: 
        _must_equal(a, b)

    assert_never



@Test.case
def test_must_equal_receives_unknwon_object_failure() -> None:

    class A:
        def __init__(self, a: int) -> None:
            self.a = a

    must_equal(A(10), A(20))



# @Test.case
# def test_sorting_works():
#     print('~~~~~~~~~~~~~~~~~~~~~~~~~')
#     ...
