from test_about_mocks.test_global_collisions.tests.test_a import \
    test_example_a_helper
from tini_test import Mock, Test, must_equal

# test_example_a_helper()


@Test.case
@Mock.mock(test_example_a_helper)
def test_example_b():
    print('I am test example_b')
    must_equal(1 + 1, 2)

