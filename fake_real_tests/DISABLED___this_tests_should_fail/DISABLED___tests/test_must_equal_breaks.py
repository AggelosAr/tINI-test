from tini_test.must_equals import must_equal
from tini_test.test_utils import Test


@Test.case
def test_multiline_string_diff_cov() -> None:
    expected = 'hello\nworld\nfoo'
    actual = 'hello\nthere\nfoo'

    must_equal(expected, actual)



@Test.case
def test_aliens_cov() -> None:
    class Pow:
        def __init__(self, xyz):
            self.a = xyz

    must_equal(Pow(123), Pow(456), lambda: 1/0)



@Test.case
def test_aliens_comp_not_given_cov() -> None:
    class Pow:
        def __init__(self, xyz):
            self.a = xyz

    must_equal(Pow(123), Pow(456))



@Test.case
def test_must_equal_receives_unknwon_object_no_comperator_provided_cov() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = 10

    must_equal(A(10), A(20))
