import io
import os

from tini_test import Isolate, Mock, Shared, Test, WillRaise, must_equal, var

# mock builtins file open

@Isolate
@Test.case
@Mock.mock(open, returns=io.StringIO('mocked content'))
def test_mock_file_open_1_returns():
    with open('file.txt', 'r') as f:
        content = f.read()
    must_equal('mocked content', content)


@Isolate
@Test.case
@Mock.mock(open, returns=io.StringIO('mocked content'))
def test_mock_file_open_2_returns():
    with open('file.txt', 'r') as f:
        content = f.read()
    must_equal('mocked content', content)


@Isolate
@Test.case
@Mock.mock(open, args=(os.path.join(os.path.dirname(__file__), 'here.txt'), 'r'))
def test_mock_file_open_args_call():

    with open('not_here.txt', 'r') as f:
        content = f.read()
    print('content IS : ', content)
    must_equal('Hello there!', content)




# TODO test shared 
# TODO test context managers
# TODO test context managers with shared
# TODO test builtints?
# @Isolate
# @Test.case
# @Shared(var.a)
# @Mock.mock(open, args=('file.txt', 'r'))
# def test_mock_file_open_args_call():
#     with open('file.txt', 'r') as f:
#         content = f.read()
#     must_equal('mocked content', content)