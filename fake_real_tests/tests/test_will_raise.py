from src.asserts import WillRaise
from src.test_suite import Test

# TODO test context on WillRaise


@Test.case
def test_will_raise_catches_correct_exception():

    with WillRaise(ZeroDivisionError) as context:
        1/0



@Test.case
def test_will_raise_catches_many_exceptions():

    with WillRaise(TypeError, ZeroDivisionError) as context:
        1/0



@Test.case
def test_will_raise_catches_from_many_exceptions_ordered_differently():

    with WillRaise(ZeroDivisionError, TypeError) as context:
        1/0



@Test.case
def test_will_raise_doesnt_catch_wrong_exception():

    def _test_will_raise_doesnt_catch_wrong_exception():
        with WillRaise(TypeError) as context:
            1/0
    
    with WillRaise(ZeroDivisionError) as context:
        _test_will_raise_doesnt_catch_wrong_exception()



@Test.case
def test_will_raise_will_not_catch_from_many_exceptions():

    def _test_will_raise_will_not_catch_from_many_exceptions():
        with WillRaise(TypeError, ValueError) as context:
            1/0

    with WillRaise(ZeroDivisionError) as context:
        _test_will_raise_will_not_catch_from_many_exceptions()
