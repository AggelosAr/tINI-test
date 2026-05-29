from typing import assert_never

from src.asserts import WillRaise
from src.utils import Test


# GG = 0

# def setup():
#     global GG
#     assert GG == 0
#     print('inside setup current val-> %d' % (GG, ))
#     GG = 1_000
#     print('inside setup updated val-> %d' % (GG, ))

# @Test.case(setup=lambda: setup())
# def test_setup_provided():
#     print('inside test_setup_provided val-----------> %d' % (GG, ))
#     assert GG == 1_000





# @Test.case
# def test_failed_test_passes_if_cought():

#     #with WillRaise(ZeroDivisionError) as context:
#         def _setup():
#             print('inside _setup')
#             1/0

#         @Test.case(setup=lambda: _setup())
#         def test_setup_provided_fails_as_a_result_test_wont_run():
#             print('this should never print')
#             assert_never()

#         test_setup_provided_fails_as_a_result_test_wont_run()





