from test_about_mocks.test_global_collisions.tests.test_a import test_example_a_helper
from tini_test.mock import Mock
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test

test_example_a_helper()


@Test.case
@Mock.mock
def test_example_c():
    print('I am test example_c')
    must_equal(1 + 1, 2)

