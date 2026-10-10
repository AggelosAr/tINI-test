from typing import assert_never

from tini_test import Test, WillRaise


@Test.case
def test_broken_test_fails():

    with WillRaise(NameError):
        print('inside test_broken_test_fails')
        _GG



@Test.case
def test_broken_test_fails_case():

    with WillRaise(TypeError):
        print('inside test_broken_test_fails_case')
        assert_never()
