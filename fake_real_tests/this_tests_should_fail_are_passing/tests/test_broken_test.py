from typing import assert_never

from small_test.context_manager import WillRaise
from src.small_test.test_suite import Test


@Test.case
def test_broken_test_fails():

    with WillRaise(NameError):
        print('inside test_broken_test_fails')
        _GG
        assert_never()


@Test.case
def test_broken_test_fails_case():
    with WillRaise(TypeError):
        print('inside test_broken_test_fails_case')
        assert_never()
