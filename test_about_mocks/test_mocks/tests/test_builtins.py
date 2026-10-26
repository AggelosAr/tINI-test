import io
import os

from tini_test import Isolate, Mock, Shared, Test, WillRaise, must_equal, var

# mock builtins file open


# Test base 
@Isolate
@Test.case
@Mock.mock(open, returns=io.StringIO('mocked content'))
def test_mock_file_open_1_returns():
    with open('?') as f:
        content = f.read()
    must_equal('mocked content', content)


@Isolate
@Test.case
@Mock.mock(open, returns=io.StringIO('mocked content'))
def test_mock_file_open_2_returns():
    with open('?') as f:
        content = f.read()
    must_equal('mocked content', content)


@Isolate
@Test.case
@Mock.mock(open, args=(os.path.join(os.path.dirname(__file__), 'here.txt'), 'r'))
def test_mock_file_open_args_call():

    with open('?') as f:
        content = f.read()

    print('content IS : ', content)
    must_equal('Hello there!', content)


# Test shared

@Test.case
@Shared(var.content)
@Mock.mock(open, returns=var.content)
def test_mock_file_open_with_shared_returns():
    var.content = io.StringIO('mocked content')

    with open('?') as f:
        content = f.read()

    must_equal('mocked content', content)

    var.content = io.StringIO('mocked contentsss')

    with open('?') as f:
        content = f.read()

    must_equal('mocked contentsss', content)




@Test.case
@Shared(var.file, var.mode)
@Mock.mock(open, args=(var.file, var.mode))
def test_mock_file_open_with_shared_args_call():
    var.file = os.path.join(os.path.dirname(__file__), 'here.txt')
    var.mode = 'r'

    with open('?') as f:
        content = f.read()

    must_equal('Hello there!', content)

    var.file = 'Not a file'

    with WillRaise(FileNotFoundError) as context:
        with open('?') as f:
            ...

    must_equal("[Errno 2] No such file or directory: 'Not a file'", str(context.exception))



# Test mocking context managers

@Isolate
@Test.case
def test_mocking_with_context_manager():

    file_one = os.path.join(os.path.dirname(__file__), 'here.txt')

    with Mock.mocking(open, args=(file_one, 'r')):

        with open('?') as f:
            content = f.read()

        must_equal('Hello there!', content)

    with WillRaise(FileNotFoundError) as context:
        with open('?') as f:
            ...

    must_equal("[Errno 2] No such file or directory: '?'", str(context.exception))

    # Run it again just to be sure!
    file_one = os.path.join(os.path.dirname(__file__), 'here.txt')
    
    with Mock.mocking(open, args=(file_one, 'r')):

        with open('?') as f:
            content = f.read()

        must_equal('Hello there!', content)

    with WillRaise(FileNotFoundError) as context:
        with open('?') as f:
            ...

    must_equal("[Errno 2] No such file or directory: '?'", str(context.exception))



@Isolate
@Test.case
def test_mocking_with_context_manager_more_nest():

    def test():

        file_one = os.path.join(os.path.dirname(__file__), 'here.txt')
        file_two = os.path.join(os.path.dirname(__file__), 'also_here.txt')

        with Mock.mocking(open, args=(file_one, 'r')):

            with Mock.mocking(open, args=(file_two, 'r')):

                with open('?') as f:
                    content = f.read()

                must_equal('Hello from the void.', content)

            with open('?') as f:
                content = f.read()

            must_equal('Hello there!', content)

        with WillRaise(FileNotFoundError) as context:
            with open('?') as f:
                ...

        must_equal("[Errno 2] No such file or directory: '?'", str(context.exception))


    test()
    test()



# Test mock and mocking with context managers with shared
@Isolate
@Test.case
@Shared(var.file_one, var.file_two)
@Mock.mock(open, args=(os.path.join(os.path.dirname(__file__), 'here.txt'), 'r'))
def test_mock_mocking_with_context_manager():

    var.file_one = os.path.join(os.path.dirname(__file__), 'here.txt')
    var.file_two = os.path.join(os.path.dirname(__file__), 'also_here.txt')

    with Mock.mocking(open, args=(var.file_one, 'r')):
    
        with Mock.mocking(open, args=(var.file_two, 'r')):

            with open('?') as f:
                content = f.read()

            must_equal('Hello from the void.', content)

        with open('?') as f:
            content = f.read()

        must_equal('Hello there!', content)

    with open('?') as f:
        content = f.read()

    must_equal('Hello there!', content)

    with Mock.mocking(open, args=(var.file_one, 'r')):
        
        with Mock.mocking(open, args=(var.file_two, 'r')):

            with open('?') as f:
                content = f.read()

            must_equal('Hello from the void.', content)

        with open('?') as f:
            content = f.read()

        must_equal('Hello there!', content)

    with open('?') as f:
        content = f.read()

    must_equal('Hello there!', content)

    def test():
        var.file_one = os.path.join(os.path.dirname(__file__), 'here.txt')
        var.file_two = os.path.join(os.path.dirname(__file__), 'also_here.txt')
    
        with Mock.mocking(open, args=(var.file_one, 'r')):
        
            with Mock.mocking(open, args=(var.file_two, 'r')):
    
                with open('?') as f:
                    content = f.read()
    
                must_equal('Hello from the void.', content)
    
            with open('?') as f:
                content = f.read()
    
            must_equal('Hello there!', content)
    
        with open('?') as f:
            content = f.read()
    
        must_equal('Hello there!', content)

    test()
    test()


    

# Test imports


# names?
# TODO test builtints?
