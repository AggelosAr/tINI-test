from src.context_manager import WillRaise
from src.misc.exceptions import WillRaiseReceivedNotAnException
from src.test_suite import Test


@Test.case
def test_will_raise_catches_correct_exception() -> None:

    with WillRaise(ZeroDivisionError) as context:
        1/0



@Test.case
def test_will_raise_catches_many_exceptions() -> None:

    with WillRaise(TypeError, ZeroDivisionError) as context:
        1/0



@Test.case
def test_will_raise_catches_from_many_exceptions_ordered_differently() -> None:

    with WillRaise(ZeroDivisionError, TypeError) as context:
        1/0



@Test.case
def test_will_raise_doesnt_catch_wrong_exception() -> None:

    def _test_will_raise_doesnt_catch_wrong_exception() -> None:
        with WillRaise(TypeError) as context:
            1/0
    
    with WillRaise(ZeroDivisionError) as context:
        _test_will_raise_doesnt_catch_wrong_exception()



@Test.case
def test_will_raise_will_not_catch_from_many_exceptions() -> None:

    def _test_will_raise_will_not_catch_from_many_exceptions() -> None:
        with WillRaise(TypeError, ValueError) as context:
            1/0

    with WillRaise(ZeroDivisionError) as context:
        _test_will_raise_will_not_catch_from_many_exceptions()



@Test.case
def test_will_raise_correclty_raises_exception() -> None:

    def _test_will_raise_correclty_raises_exception() -> None:
        with WillRaise(1, None, Exception) as context:
            ...

    with WillRaise(WillRaiseReceivedNotAnException) as context:
        _test_will_raise_correclty_raises_exception()
