from test_global_collisions.tests.test_a import test_example_a_helper
from tini_test.mock import Mock
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test

# test_example_a_helper()


@Test.case
@Mock.mock(test_example_a_helper)
def test_example_b():
    print('I am test example_b')
    must_equal(1 + 1, 2)

