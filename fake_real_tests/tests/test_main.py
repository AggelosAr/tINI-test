from typing import assert_never

from src.asserts import AssertRaises
from src.utils import Test

# TODO add docs on starting to write with parenthesis
# TODO call function inside
# TODO assert fail e.g. 1/0 inside the test and seert it is fail
# TODO add some tests with db ?
# TODO test context on AssertRaises

@Test.case
def test_decorator_works_no_parenthesis():
    ...


@Test.case()
def test_decorator_works_parenthesis():
    ...


GG = 0

def setup():
    global GG
    print('setup called GG-> %d' % (GG, ))
    GG = 1_000
    print('setup called GG-> %d' % (GG, ))

@Test.case(setup=lambda: setup())
def test_setup_provided():
    print('inside test_setup_provided GG-----------> %d' % (GG, ))
    assert GG == 1_000




_GG = 999

def cleanup():
    global _GG
    _GG = 2_000
    print('cleanup called -> %d' % (GG, ))

@Test.case(cleanup=lambda: cleanup())
def test_cleanup_provided():
    assert _GG == 999
# TODO 
# assert _GG == 2_000


__GG = 0

def _setup():
    global __GG
    __GG = -10
    print('_setup called -> %d' % (GG, ))

def _cleanup():
    global __GG
    __GG = 10
    print('_cleanup called -> %d' % (GG, ))

@Test.case(setup=lambda: _setup(), cleanup=lambda: _cleanup())
def test_setup_cleanup_provided():
    print('This should show !~')
    assert __GG == -10
# TODO 
#assert __GG == 10


@Test.case
def test_assert_raises_catches_correct_exception():

    with AssertRaises(ZeroDivisionError) as context:
        1/0

@Test.case
def test_assert_raises_doesnt_catch_wrong_exception():

    def _test_assert_raises_doesnt_catch_wrong_exception():
        with AssertRaises(TypeError) as context:
            1/0
    
    with AssertRaises(ZeroDivisionError) as context:
        _test_assert_raises_doesnt_catch_wrong_exception()


@Test.case
def test_assert_raises_catches_from_many_exceptions():

    with AssertRaises(TypeError, ZeroDivisionError) as context:
        1/0


@Test.case
def test_assert_raises_catches_from_many_exceptions_ordered_differently():

    with AssertRaises(ZeroDivisionError, TypeError) as context:
        1/0


@Test.case
def test_assert_raises_will_not_catch_from_many_exceptions():

    def _test_assert_raises_will_not_catch_from_many_exceptions():
        with AssertRaises(TypeError, ValueError) as context:
            1/0

    with AssertRaises(ZeroDivisionError) as context:
        _test_assert_raises_will_not_catch_from_many_exceptions()