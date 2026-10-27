from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
    func_c


def func_b(*args, **kwargs):

    return 1 + func_c(*args, **kwargs)




def B_open(*args, **kwargs):
    with open('?') as f:
        return f.read()


def B_open_MOCKING(*args, **kwargs):
    from tini_test import Mock, must_equal, var

    with open(var.root, 'r') as f:
        must_equal('inside B', f.read())

    with Mock.mocking(open, args=(var.root, 'r')) as f:
        with open('?') as f:
            res = f.read()

    with open(var.root, 'r') as f:
        must_equal('inside B', f.read())

    return res