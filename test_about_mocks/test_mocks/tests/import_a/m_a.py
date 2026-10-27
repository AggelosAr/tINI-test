from test_about_mocks.test_mocks.tests.import_a.import_b.m_b import func_b

from tini_test import Mock, var, must_equal


def func_a(*args, **kwargs):

    return 1 + func_b(*args, **kwargs)




def A_open(*args, **kwargs):
    with open('?') as f:
        return f.read()


def A_open_MOCKING(*args, **kwargs):

    with open(var.root, 'r') as f:
        must_equal('inside A', f.read())

    with Mock.mocking(open, args=(var.root, 'r')) as f:
        with open('?') as f:
            res = f.read()

    with open(var.root, 'r') as f:
        must_equal('inside A', f.read())

    return res
