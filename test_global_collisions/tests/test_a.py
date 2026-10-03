from tini_test.mock import Mock
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test


def test_example_a_helper():
    print('I am test example_a helper')



@Test.case
@Mock.mock
def test_example_a():
    print('I am test example_a')
    must_equal(1 + 1, 2)



