from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
    func_c


def func_b(*args, **kwargs):

    return 1 + func_c(*args, **kwargs)
