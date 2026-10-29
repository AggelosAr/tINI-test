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
@Isolate
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
                res = f.read()
                print('CONTENT IS : ', res)

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
def X_test_imported_builtin_open():
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


    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'b.txt')
    must_equal('inside B', A_open())
    must_equal('inside B', B_open())
    must_equal('inside B', C_open())

    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'a.txt')
    must_equal('inside A', A_open())
    must_equal('inside A', B_open())
    must_equal('inside A', C_open())

    
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


    with WillRaise(FileNotFoundError):
        res = A_open()

    with WillRaise(FileNotFoundError):
        B_open()

    with WillRaise(FileNotFoundError):
        C_open()


# Test returns 

@Isolate
@Test.case
@Shared(var.root)
def test_MOCKING_ABC_returns():

    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'a.txt')

    with Mock.mocking(open, returns='step 1') as f:
        from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
            C_open
        from test_about_mocks.test_mocks.tests.import_a.import_b.m_b import \
            B_open
        from test_about_mocks.test_mocks.tests.import_a.m_a import A_open

        with WillRaise(TypeError) as context:
            must_equal('step 1', A_open())
            must_equal('step 1', B_open())
            must_equal('step 1', C_open())

        # XXX Y  from 3.12 to 3.12 ++ (missed __exit__ method) Python version: 3.12.13
        print(str(context.exception))
        must_equal("'str' object does not support the context manager protocol", str(context.exception))

    with Mock.mocking(open, returns=io.StringIO('step 1')) as f:
        from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
            C_open
        from test_about_mocks.test_mocks.tests.import_a.import_b.m_b import \
            B_open
        from test_about_mocks.test_mocks.tests.import_a.m_a import A_open

        must_equal('step 1', A_open())

    with Mock.mocking(open, returns=io.StringIO('step 1')) as f:
        must_equal('step 1', B_open())

    with Mock.mocking(open, returns=io.StringIO('step 1')) as f:
        must_equal('step 1', C_open())

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


    with WillRaise(FileNotFoundError):
        res = A_open()

    with WillRaise(FileNotFoundError):
        B_open()

    with WillRaise(FileNotFoundError):
        C_open()




@Isolate
@Test.case
@Shared(var.root)
def test_built_in_refreshes():
    from test_about_mocks.test_mocks.tests.import_a.m_a import (A_open,
                                                                A_open_MOCKING)
    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'a.txt')
    with Mock.mocking(open, returns=io.StringIO('step 1')) as f:
        must_equal('step 1', A_open())
        must_equal('step 1', A_open())


    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'a.txt')
    must_equal('inside A', A_open_MOCKING())
    must_equal('inside A', A_open_MOCKING())

    with Mock.mocking(open, args=(var.root, 'r')) as f:
        with open('?') as f:
            must_equal('inside A', f.read())
        with open('?') as f:
            must_equal('inside A', f.read())


    with Mock.mocking(open, returns=io.StringIO('step 1')) as f:
        with Mock.mocking(open, args=(var.root, 'r')) as f:
            with open('?') as f:
                must_equal('inside A', f.read())
        with open('?') as f:
            must_equal('step 1', f.read())   

    with Mock.mocking(open, returns=io.StringIO('step 1')) as f:
        with open('?') as f:
            must_equal('step 1', f.read())

    with Mock.mocking(open, returns=io.StringIO('step 1')) as f:
        with open('?') as f:
            must_equal('step 1', f.read())

    with Mock.mocking(open, returns=io.StringIO('step 1')) as f:
        with open('?') as f:
            must_equal('step 1', f.read())
        with open('?') as f:
            must_equal('step 1', f.read())



#    //////////////// //////////////// //////////////// //////////////// //////////////// //////////////// 
#   //////////////// //////////////// //////////////// //////////////// //////////////// //////////////// 
#  //////////////// //////////////// //////////////// //////////////// //////////////// //////////////// 
# //////////////// test more builtints ///////////// //////////////// //////////////// //////////////// 
#    //////////// //////////////// //////////////// //////////////// //////////////// //////////////// 
#   //////////// //////////////// //////////////// //////////////// //////////////// //////////////// 
#  //////////// //////////////// //////////////// //////////////// //////////////// //////////////// 

@Isolate
@Test.case
@Mock.mock(len, args=((1, 2, 3), ))
def test_len_as_different_name():
    ___len = len
    must_equal(3, ___len('?'))




@Isolate
@Test.case
@Mock.mock(len, args=((1, 2, 3), ))
def test_len():
    must_equal(3, len('?'))

    # Test import
    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
        _len
    must_equal(3 + 3, _len('?'))

    # Test mocking
    with Mock.mocking(len, args=((1, 2, 3, 4), )) as f:
        must_equal(4, len('?'))


# ///////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////
# IMPORTANT TESTS: XXX
@Isolate
@Test.case
@Mock.mock(len, args=((1, 2, 3), ))
def test_call_graph_patch_with_mock():
    must_equal(3, len('?'))

    # Test import
    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
        _len
    must_equal(3 + 3, _len('?'))
    
    # Test mocking
    with Mock.mocking(len, args=((1, ), )) as f:
        must_equal(1, len('?'))
        must_equal(1 + 1, _len('?'))

        with Mock.mocking(_len, args=((1, 2, ), )) as g:
            must_equal(1, len('?'))
            must_equal(1 + 1, _len('?'))

            with Mock.mocking(_len, args=((1, 2, 3, ), )) as g:
                must_equal(1, len('?'))
                must_equal(1 + 1, _len('?'))

            must_equal(1, len('?'))
            must_equal(1 + 1, _len('?'))

        must_equal(1, len('?'))
        must_equal(1 + 1, _len('?'))


    must_equal(3, len('?'))
    must_equal(3 + 3, _len('?'))


@Isolate
@Test.case
def test_call_graph_patch_no_mock():
    must_equal(1, len('?'))

    # Test import
    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
        _len
    must_equal(1, _len('?'))
    
    # Test mocking
    with Mock.mocking(len, args=((1, ), )) as f:
        must_equal(1, len('?'))
        must_equal(1 + 1, _len('?'))

        with Mock.mocking(_len, args=((1, 2, ), )) as g:
            must_equal(1, len('?'))
            must_equal(1 + 1, _len('?'))

            with Mock.mocking(_len, args=((1, 2, 3, ), )) as g:
                must_equal(1, len('?'))
                must_equal(1 + 1, _len('?'))

            must_equal(1, len('?'))
            must_equal(1 + 1, _len('?'))

        must_equal(1, len('?'))
        must_equal(1 + 1, _len('?'))

    must_equal(1, len('?'))
    must_equal(1, _len('?'))


# XXX what do we do in this case ???????
# def xyz(args):
#     return len(args)

# @Isolate
# @Test.case
# @Mock.mock(xyz, args=((1, 2, 3), ))
# def test_call_graph_patch_normal():
#     must_equal(3, xyz('?'))

#     # Test import
#     from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import _xyz
#     must_equal(1, _xyz('?'))

#     # Test mocking
#     with Mock.mocking(xyz, args=((1, ), )) as f:
#         must_equal(1, xyz('?'))
#         must_equal(1 + 1, _xyz('?'))

#         with Mock.mocking(_xyz, args=((1, 2, ), )) as g:
#             must_equal(2, xyz('?'))
#             must_equal(2 + 2, _xyz('?'))

#             with Mock.mocking(_xyz, args=((1, 2, 3, ), )) as g:
#                 must_equal(3, xyz('?'))
#                 must_equal(3 + 3, _xyz('?'))

#             must_equal(2, xyz('?'))
#             must_equal(2 + 2, _xyz('?'))

#         must_equal(1, xyz('?'))
#         must_equal(1 + 1, _xyz('?'))

#     must_equal(3, xyz('?'))
#     must_equal(3 + 3, _xyz('?'))
# ///////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////



@Isolate
@Test.case
@Mock.mock(abs, args=(-5,))
def test_abs():
    must_equal(5, abs(0))

    # Test mocking
    with Mock.mocking(abs, args=(-15,)) as f:
        must_equal(15, abs(0))


@Isolate
@Test.case
@Mock.mock(all, args=([True, True],))
def test_all():
    must_equal(True, all([False]))

    # Test mocking
    with Mock.mocking(all, args=([True, True, True],)) as f:
        must_equal(True, all([False]))


@Isolate
@Test.case
@Mock.mock(any, args=([False, True],))
def test_any():
    must_equal(True, any([]))

    # Test mocking
    with Mock.mocking(any, args=([False, False, True],)) as f:
        must_equal(True, any([]))
    


@Isolate
@Test.case
@Mock.mock(ascii, args=('hello',))
def test_ascii():
    must_equal("'hello'", ascii('other'))

    # Test mocking
    with Mock.mocking(ascii, args=('other',)) as f:
        must_equal("'other'", ascii('hello'))


@Isolate
@Test.case
@Mock.mock(bin, args=(10,))
def test_bin():
    must_equal('0b1010', bin(0))

    # Test mocking
    with Mock.mocking(bin, args=(5,)) as f:
        must_equal('0b101', bin(0))


@Isolate
@Test.case
@Mock.mock(bool, args=(1,))
def test_bool():
    must_equal(True, bool(0))

    # Test mocking
    with Mock.mocking(bool, args=(False,)) as f:
        must_equal(False, bool(1))


@Isolate
@Test.case
@Mock.mock(callable, args=(lambda: None,))
def test_callable():
    must_equal(True, callable(123))

    # Test mocking
    with Mock.mocking(callable, args=(lambda: None,)) as f:
        must_equal(True, callable(123))


@Isolate
@Test.case
@Mock.mock(chr, args=(65,))
def test_chr():
    must_equal('A', chr(0))

    # Test mocking
    with Mock.mocking(chr, args=(66,)) as f:
        must_equal('B', chr(0))


@Isolate
@Test.case
@Mock.mock(complex, args=(1, 2))
def test_complex():
    must_equal(1 + 2j, complex(0))

    # Test mocking
    with Mock.mocking(complex, args=(2, 3)) as f:
        must_equal(2 + 3j, complex(0))


@Isolate
@Test.case
@Mock.mock(dict, args=({'a': 1},))
def test_dict():
    must_equal({'a': 1}, dict())

    # Test mocking
    with Mock.mocking(dict, args=({'b': 2},)) as f:
        must_equal({'b': 2}, dict())


@Isolate
@Test.case
@Mock.mock(divmod, args=(10, 3))
def test_divmod():
    must_equal((3, 1), divmod(1, 1))

    # Test mocking
    with Mock.mocking(divmod, args=(20, 4)) as f:
        must_equal((5, 0), divmod(1, 1))


@Isolate
@Test.case
@Mock.mock(float, args=('1.5',))
def test_float():
    must_equal(1.5, float(0))

    # Test mocking
    with Mock.mocking(float, args=('2.5',)) as f:
        must_equal(2.5, float(0))


@Isolate
@Test.case
@Mock.mock(format, args=(10, '04d'))
def test_format():
    must_equal('0010', format(0))

    # Test mocking
    with Mock.mocking(format, args=(5, '02d')) as f:
        must_equal('05', format(0))


@Isolate
@Test.case
@Mock.mock(frozenset, args=([1, 2],))
def test_frozenset():
    must_equal(frozenset({1, 2}), frozenset())

    # Test mocking
    with Mock.mocking(frozenset, args=([3, 4],)) as f:
        must_equal(frozenset({3, 4}), frozenset())


@Isolate
@Test.case
@Mock.mock(hash, args=('hello',))
def test_hash():
    must_equal(hash('hello'), hash('other'))

    # Test mocking
    with Mock.mocking(hash, args=('other',)) as f:
        must_equal(hash('other'), hash('?'))


@Isolate
@Test.case
@Mock.mock(hex, args=(255,))
def test_hex():
    must_equal('0xff', hex(0))

    # Test mocking
    with Mock.mocking(hex, args=(128,)) as f:
        must_equal('0x80', hex(0))


@Isolate
@Test.case
@Mock.mock(int, args=('42',))
def test_int():
    must_equal(42, int(0))

    # Test mocking
    with Mock.mocking(int, args=('100',)) as f:
        must_equal(100, int(0))


@Isolate
@Test.case
@Mock.mock(list, args=((1, 2, 3),))
def test_list():
    print('-------> ', list())
    must_equal([1, 2, 3], list())

    # Test mocking
    with Mock.mocking(list, args=((4, 5, 6),)) as f:
        must_equal([4, 5, 6], list())

    must_equal([1, 2, 3], list())


@Isolate
@Test.case
@Mock.mock(max, args=((1, 2, 3),))
def test_max():
    must_equal(3, max(0))

    # Test mocking
    with Mock.mocking(max, args=((4, 5, 6),)) as f:
        must_equal(6, max(0))


@Isolate
@Test.case
@Mock.mock(min, args=((1, 2, 3),))
def test_min():
    must_equal(1, min(0))

    # Test mocking
    with Mock.mocking(min, args=((4, 5, 6),)) as f:
        must_equal(4, min(0))


@Isolate
@Test.case
@Mock.mock(oct, args=(8,))
def test_oct():
    must_equal('0o10', oct(0))

    # Test mocking
    with Mock.mocking(oct, args=(16,)) as f:
        must_equal('0o20', oct(0))


@Isolate
@Test.case
@Mock.mock(pow, args=(2, 3))
def test_pow():
    must_equal(8, pow(1, 1))

    # Test mocking
    with Mock.mocking(pow, args=(3, 2)) as f:
        must_equal(9, pow(1, 1))


@Isolate
@Test.case
@Mock.mock(repr, args=('hello',))
def test_repr():
    must_equal("'hello'", repr(0))

    # Test mocking
    with Mock.mocking(repr, args=('world',)) as f:
        must_equal("'world'", repr(0))


@Isolate
@Test.case
@Mock.mock(round, args=(3.14159, 2))
def test_round():
    must_equal(3.14, round(0))

    # Test mocking
    with Mock.mocking(round, args=(2.71828, 2)) as f:
        must_equal(2.72, round(0))


@Isolate
@Test.case
@Mock.mock(set, args=([1, 2, 2],))
def test_set():
    must_equal({1, 2}, set())

    # Test mocking
    with Mock.mocking(set, args=([3, 4, 4],)) as f:
        must_equal({3, 4}, set())


@Isolate
@Test.case
@Mock.mock(str, args=(123,))
def test_str():
    must_equal('123', str(0))

    # Test mocking
    with Mock.mocking(str, args=('456',)) as f:
        must_equal('456', str(0))


@Isolate
@Test.case
@Mock.mock(sum, args=([1, 2, 3],))
def test_sum():
    must_equal(6, sum([]))

    # Test mocking
    with Mock.mocking(sum, args=([4, 5, 6],)) as f:
        must_equal(15, sum([]))


@Isolate
@Test.case
@Mock.mock(tuple, args=([1, 2, 3],))
def test_tuple():
    must_equal((1, 2, 3), tuple())

    # Test mocking
    with Mock.mocking(tuple, args=([4, 5, 6],)) as f:
        must_equal((4, 5, 6), tuple())


@Isolate
@Test.case
@Mock.mock(type, args=(123,))
def test_type():
    must_equal(int, type('hello'))

    # Test mocking
    with Mock.mocking(type, args=(str,)) as f:
        must_equal(type(str), type(1))


@Isolate
@Test.case
@Mock.mock(sorted, args=([3, 1, 2],))
def test_sorted():
    must_equal([1, 2, 3], sorted([]))

    # Test mocking
    with Mock.mocking(sorted, args=([4, 2, 1],)) as f:
        must_equal([1, 2, 4], sorted([]))


@Isolate
@Test.case
@Mock.mock(reversed, args=((1, 2, 3),))
def test_reversed():
    must_equal([3, 2, 1], list(reversed([])))

    # Test mocking
    with Mock.mocking(reversed, args=((4, 5, 6),)) as f:
        must_equal([6, 5, 4], list(reversed([])))


@Isolate
@Test.case
@Mock.mock(enumerate, args=(('a', 'b'),))
def test_enumerate():
    must_equal([(0, 'a'), (1, 'b')], list(enumerate([])))

    # Test mocking
    with Mock.mocking(enumerate, args=(('x', 'y'),)) as f:
        must_equal([(0, 'x'), (1, 'y')], list(enumerate([])))


@Isolate
@Test.case
@Mock.mock(zip, args=((1, 2), ('a', 'b')))
def test_zip():
    # print('---------> ', list(zip([], [])))
    must_equal([(1, 'a'), (2, 'b')], list(zip([], [])))

    # Test mocking
    with Mock.mocking(zip, args=((3, 4), ('c', 'd'))) as f:
        must_equal([(3, 'c'), (4, 'd')], list(zip([], [])))


@Isolate
@Test.case
@Mock.mock(map, args=(str, (1, 2, 3)))
def test_map():
    must_equal(['1', '2', '3'], list(map(str, [])))

    # Test mocking
    with Mock.mocking(map, args=(str, (4, 5, 6))) as f:
        must_equal(['4', '5', '6'], list(map(str, [])))


@Isolate
@Test.case
@Mock.mock(filter, args=(bool, (0, 1, 2)))
def test_filter():
    must_equal([1, 2], list(filter(bool, [])))

    # Test mocking
    with Mock.mocking(filter, args=(bool, (3, 0, 4))) as f:
        must_equal([3, 4], list(filter(bool, [])))


@Isolate
@Test.case
@Mock.mock(range, args=(3,))
def test_range():
    must_equal([0, 1, 2], list(range(0)))

    # Test mocking
    with Mock.mocking(range, args=(5,)) as f:
        must_equal([0, 1, 2, 3, 4], list(range(0)))


@Isolate
@Test.case
@Mock.mock(ord, args=('A',))
def test_ord():
    must_equal(65, ord('B'))

    # Test mocking
    with Mock.mocking(ord, args=('B',)) as f:
        must_equal(66, ord('A'))


@Isolate
@Test.case
@Mock.mock(bytes, args=('abc', 'utf-8'))
def test_bytes():
    must_equal(b'abc', bytes())

    # Test mocking
    with Mock.mocking(bytes, args=('def', 'utf-8')) as f:
        must_equal(b'def', bytes())


@Isolate
@Test.case
@Mock.mock(bytearray, args=('abc', 'utf-8'))
def test_bytearray():
    must_equal(bytearray(b'abc'), bytearray())

    # Test mocking
    with Mock.mocking(bytearray, args=('def', 'utf-8')) as f:
        must_equal(bytearray(b'def'), bytearray())


@Isolate
@Test.case
@Mock.mock(slice, args=(1, 5, 2))
def test_slice():
    s = slice(0, 0)
    must_equal((1, 5, 2), (
        slice(s).start,
        slice(s).stop,
        slice(s).step,
    ))

    # Test mocking
    with Mock.mocking(slice, args=(2, 6, 3)) as f:
        s = slice(0, 0)
        must_equal((2, 6, 3), (
            slice(s).start,
            slice(s).stop,
            slice(s).step,
        ))


@Isolate
@Test.case
@Mock.mock(isinstance, args=(1, int))
def test_isinstance():
    must_equal(True, isinstance('?'))

    # Test mocking
    with Mock.mocking(isinstance, args=(2, int)) as f:
        must_equal(True, isinstance(2, str))


@Isolate
@Test.case
@Mock.mock(issubclass, args=(bool, int))
def test_issubclass():
    must_equal(True, issubclass('?'))

    # Test mocking
    with Mock.mocking(issubclass, args=(int, int)) as f:
        must_equal(True, issubclass('?'))



class Dummy:
    pass

class DummyWithAttr:
    def __init__(self):
        self.x = 42
        self.y = 84
        
@Isolate
@Test.case
@Mock.mock(getattr, args=(DummyWithAttr(), 'x'))
def test_getattr():
    must_equal(42, getattr('?'))

    # Test mocking
    with Mock.mocking(getattr, args=(DummyWithAttr(), 'y')) as f:
        must_equal(84, getattr('?'))


@Isolate
@Test.case
@Mock.mock(hasattr, args=(DummyWithAttr(), 'x'))
def test_hasattr():
    must_equal(True, hasattr(Dummy, 'x'))

    # Test mocking
    with Mock.mocking(hasattr, args=(DummyWithAttr(), 'z')) as f:
        must_equal(False, hasattr('?'))


@Isolate
@Test.case
@Mock.mock(callable, args=(print,))
def test_callable_builtin():
    must_equal(True, callable('?'))

    # Test mocking
    with Mock.mocking(callable, args=(len,)) as f:
        must_equal(True, callable('?'))

