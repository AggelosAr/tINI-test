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


@Isolate
@Test.case
@Shared(var.root)
def test_imported_builtin_open():
    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.closure_mocking_utils import \
        test_imported_builtin_open
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
        from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.closure_mocking_utils import \
            test_imported_builtin_open
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




# Test updating built-in open with Mock
# On various places. 

@Isolate
@Test.case
@Shared(var.root)
@Mock.mock(open, args=(var.root, 'r'))
def MOCK_A_OPEN():
    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'a.txt')
    from test_about_mocks.test_mocks.tests.import_a.m_a import A_open
    must_equal('inside A', A_open())


@Isolate
@Test.case
@Shared(var.root)
@Mock.mock(open, args=(var.root, 'r'))
def MOCK_B_OPEN():
    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'b.txt')
    from test_about_mocks.test_mocks.tests.import_a.import_b.m_b import B_open
    must_equal('inside B', B_open())



@Isolate
@Test.case
@Shared(var.root)
@Mock.mock(open, args=(var.root, 'r'))
def MOCK_C_OPEN():
    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'c.txt')
    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
        C_open
    must_equal('inside C', C_open())



@Isolate
@Test.case
@Shared(var.root)
@Mock.mock(open, args=(var.root, 'r'))
def test_MOCK_ABC():
    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'a.txt')
    from test_about_mocks.test_mocks.tests.import_a.m_a import A_open
    must_equal('inside A', A_open())

    from test_about_mocks.test_mocks.tests.import_a.import_b.m_b import B_open
    must_equal('inside A', B_open())

    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
        C_open
    must_equal('inside A', C_open())

    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'b.txt')
    with Mock.mocking(open, args=(var.root, 'r')) as f:
        from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
            C_open
        from test_about_mocks.test_mocks.tests.import_a.import_b.m_b import \
            B_open
        from test_about_mocks.test_mocks.tests.import_a.m_a import A_open
        must_equal('inside B', A_open())
        must_equal('inside B', B_open())
        must_equal('inside B', C_open())

    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'c.txt')
    with Mock.mocking(open, args=(var.root, 'r')) as f:
        from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
            C_open
        from test_about_mocks.test_mocks.tests.import_a.import_b.m_b import \
            B_open
        from test_about_mocks.test_mocks.tests.import_a.m_a import A_open
        must_equal('inside C', A_open())
        must_equal('inside C', B_open())
        must_equal('inside C', C_open())


    with WillRaise(TypeError):
        A_open()

    with WillRaise(TypeError):
        B_open()

    with WillRaise(TypeError):
        C_open()

# Test updating built-in open with Mocking
# On various places.

@Isolate
@Test.case
@Shared(var.root)
def MOCKING_A_OPEN():
    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'a.txt')
    from test_about_mocks.test_mocks.tests.import_a.m_a import A_open_MOCKING
    must_equal('inside A', A_open_MOCKING())


@Isolate
@Test.case
@Shared(var.root)
def MOCKING_B_OPEN():
    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'b.txt')
    from test_about_mocks.test_mocks.tests.import_a.import_b.m_b import \
        B_open_MOCKING
    must_equal('inside B', B_open_MOCKING())



@Isolate
@Test.case
@Shared(var.root)
def MOCKING_C_OPEN():
    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'c.txt')
    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
        C_open_MOCKING
    must_equal('inside C', C_open_MOCKING())




@Isolate
@Test.case
@Shared(var.root)
def test_MOCKING_ABC():

    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'a.txt')

    with Mock.mocking(open, args=(var.root, 'r')) as f:
        from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
            C_open
        from test_about_mocks.test_mocks.tests.import_a.import_b.m_b import \
            B_open
        from test_about_mocks.test_mocks.tests.import_a.m_a import A_open
        must_equal('inside A', A_open())
        must_equal('inside A', B_open())
        must_equal('inside A', C_open())


    from test_about_mocks.test_mocks.tests.import_a.m_a import A_open_MOCKING
    must_equal('inside A', A_open_MOCKING())
    print('[--------- A PASSED ---------]')

    
    from test_about_mocks.test_mocks.tests.import_a.import_b.m_b import \
        B_open_MOCKING
    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'b.txt')
    must_equal('inside B', B_open_MOCKING())
    print('[--------- B PASSED ---------]')

    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
        C_open_MOCKING
    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'c.txt')
    must_equal('inside C', C_open_MOCKING())
    print('[--------- C PASSED ---------]')


    with WillRaise(TypeError):
        A_open()

    with WillRaise(TypeError):
        B_open()

    with WillRaise(TypeError):
        C_open()


# names?
# TODO test more builtints?
# TODO add 1 big test as the last with returns 
# TODO add 1 test where u globally import instead of inside functions