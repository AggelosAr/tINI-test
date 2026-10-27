
'''

...........


'''
import os

from tini_test import Isolate, Mock, Shared, Test, WillRaise, must_equal, var



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

    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import C_open
    must_equal('inside A', C_open())

    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'b.txt')
    with Mock.mocking(open, args=(var.root, 'r')) as f:
        from test_about_mocks.test_mocks.tests.import_a.m_a import A_open
        from test_about_mocks.test_mocks.tests.import_a.import_b.m_b import B_open
        from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import C_open
        must_equal('inside B', A_open())
        must_equal('inside B', B_open())
        must_equal('inside B', C_open())

    var.root = os.path.join(os.path.dirname(__file__), 'txts', 'c.txt')
    with Mock.mocking(open, args=(var.root, 'r')) as f:
        from test_about_mocks.test_mocks.tests.import_a.m_a import A_open
        from test_about_mocks.test_mocks.tests.import_a.import_b.m_b import B_open
        from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import C_open
        must_equal('inside C', A_open())
        must_equal('inside C', B_open())
        must_equal('inside C', C_open())


    with WillRaise(TypeError):
        A_open()

    with WillRaise(TypeError):
        B_open()

    with WillRaise(TypeError):
        C_open()
