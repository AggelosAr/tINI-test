from tini_test.context_manager import WillRaise
from tini_test.misc.exceptions import (ExceptionWasNotRaised,
                                        WillRaiseReceivedNotAnException)
from tini_test.must_equals import must_equal
from tini_test.test_suite import Test


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
    
    with WillRaise(ExceptionWasNotRaised) as context:
        _test_will_raise_doesnt_catch_wrong_exception()



@Test.case
def test_will_raise_will_not_catch_from_many_exceptions() -> None:

    def _test_will_raise_will_not_catch_from_many_exceptions() -> None:
        with WillRaise(TypeError, ValueError) as context:
            1/0

    with WillRaise(ExceptionWasNotRaised) as context:
        _test_will_raise_will_not_catch_from_many_exceptions()



@Test.case
def test_will_raise_correclty_initializes() -> None:

    def _test_will_raise_correclty_raises_exception() -> None:
        with WillRaise(1, None, Exception) as context:
            ...

    with WillRaise(WillRaiseReceivedNotAnException) as context:
        _test_will_raise_correclty_raises_exception()



@Test.case()
def test_will_raise_not_raised_exception_correctly_stops_the_test() -> None:

    x = [6_000_000]

    def assert_excecution_is_stopped_on_will_raise(y):

        print('This will show. And since an exception is not raised, it errors.')

        with WillRaise(TypeError) as context:
            ...

        print('This will never show.')
        y[0] = 9_000_000


    print('This will print since we catch the incoming exception.')
    with WillRaise(ExceptionWasNotRaised) as context:
        assert_excecution_is_stopped_on_will_raise(x)

    must_equal([6_000_000], x)
