from tini_test import Mock, Test, must_equal


def test_example_a_helper():
    print('I am test example_a helper')



@Test.case
@Mock.mock
def test_example_a():
    print('I am test example_a')
    must_equal(1 + 1, 2)



