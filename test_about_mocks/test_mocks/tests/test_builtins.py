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


    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

    

# Test imports

# XXX 
# Very important test 
# Add tests for returns and functions. Test closure transfer... Move it to a seperate file.?

@Isolate
@Test.case
def sanity_check():
    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import test_imported_x_function

    must_equal(1 + 100, test_imported_x_function(1, use_mock=True))

    must_equal(2 + 200, test_imported_x_function(2, use_mock=False))

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def test():
        from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import test_imported_x_function
    
        must_equal(1 + 100, test_imported_x_function(1, use_mock=True))
    
        must_equal(2 + 200, test_imported_x_function(2, use_mock=False))

    test()
    test()

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////



# TODO are we updating the wrong globals ???????? 

@Isolate
@Test.case
@Shared(var.root)
def test_imported_builtin_open():
    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import test_imported_builtin_open
    var.root = os.path.dirname(__file__)

    with WillRaise(FileNotFoundError) as context:
        must_equal('Hello from the void.', test_imported_builtin_open('not_extisting.txt', use_mock=True))

    __path = os.path.join(var.root, 'not_extisting.txt')
    must_equal("[Errno 2] No such file or directory: '%s'" % __path, str(context.exception))

    must_equal('Hello from the void.', test_imported_builtin_open('also_here.txt', use_mock=False))

    with Mock.mocking(open, args=(os.path.join(var.root, 'here.txt'), 'r')):
        must_equal('Hello there!', test_imported_builtin_open('?', use_mock=False))

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def test():
        from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import test_imported_builtin_open
        var.root = os.path.dirname(__file__)

        with WillRaise(FileNotFoundError) as context:
            must_equal('Hello from the void.', test_imported_builtin_open('not_extisting.txt', use_mock=True))
    
        __path = os.path.join(var.root, 'not_extisting.txt')
        must_equal("[Errno 2] No such file or directory: '%s'" % __path, str(context.exception))

        must_equal('Hello from the void.', test_imported_builtin_open('also_here.txt', use_mock=False))
    
        with Mock.mocking(open, args=(os.path.join(var.root, 'here.txt'), 'r')):
            must_equal('Hello there!', test_imported_builtin_open('?', use_mock=False))

    test()
    test()

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////




# TODO add  a test like the previous with Mock.mock to test globals 



# names?
# TODO test builtints?
