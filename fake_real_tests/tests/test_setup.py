from typing import assert_never

from src.context_manager import WillRaise
from src.test_suite import Test

GG = 0

def setup():
    global GG
    assert GG == 0
    print('inside setup current val-> %d' % (GG, ))
    GG = 1_000
    print('inside setup updated val-> %d' % (GG, ))

@Test.case(setup=lambda: setup())
def test_setup_provided():
    print('inside test_setup_provided val-----------> %d' % (GG, ))
    assert GG == 1_000



# TODO create smt to make this test pass. This is the correct behaviour
# This test should fail.
# def _setup():
#     print('inside _setup')
#     1/0

# @Test.case(setup=lambda: _setup())
# def test_setup_provided_fails_as_a_result_test_wont_run():
#     print('this should never print')
#     assert_never()





