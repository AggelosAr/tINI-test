from typing import assert_never

from tini_test.context_managers import WillRaise
from tini_test.misc.exceptions import ExpectedWasDifferentFromActual
from tini_test.must_equals import must_equal
from tini_test.test import Test


@Test.case
def test_broken_test_case_one():

    with WillRaise(ZeroDivisionError):
        print('test_broken_test_case_one')
        1/0



def setup_breaks():
    with WillRaise(ZeroDivisionError):
        print('setup_breaks---->This should print and fail the test, but is was caught')
        1/0
        
@Test.case(setup=lambda: setup_breaks())
def test_setup_breaks():
    
    with WillRaise(TypeError):
        assert_never()

    print('test_setup_breaks---->This should never print, but setup_breaks was caught and will run')




def cleanup_breaks():
    with WillRaise(ZeroDivisionError):
        print('cleanup_breaks---->This should print and fail the test, but is was caught')
        1/0
@Test.case(cleanup=lambda: cleanup_breaks())
def test_cleanup_breaks():
    print('test_cleanup_breaks---->This should print and then the clean up will divide by zero')



def _cleanup_breaks():
    with WillRaise(TypeError) as context: 
        print('_cleanup_breaks---->This should never print. BUT it will!')
        assert_never()


@Test.case(setup=lambda: setup_breaks(), 
           cleanup=lambda: _cleanup_breaks())
def test_cleanup_breaks_test_and_break_down_wont_run():

    with WillRaise(TypeError) as context: 
        print('---->This should never print, but it did!')
        assert_never()



@Test.case
def test_will_raise_fails_to_catch_exception() -> None:
    a = 0.1 + 0.2
    b = 0.3

    with WillRaise(ExpectedWasDifferentFromActual) as context: 
        must_equal(a, b)

    with WillRaise(IndexError) as context: 
        x = [0, 1]
        x[1_000_000]

    with WillRaise(KeyError) as context: 
        y = {'a': a}
        y[a] # type: ignore[index]
