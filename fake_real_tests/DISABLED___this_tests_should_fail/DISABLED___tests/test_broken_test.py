from typing import assert_never

from tini_test.test import Test


@Test.case
def test_broken_test_fails():
    print('inside test_broken_test_fails')
    _GG



@Test.case
def test_broken_test_fails_case():
    print('inside test_broken_test_fails_case')
    assert_never()
