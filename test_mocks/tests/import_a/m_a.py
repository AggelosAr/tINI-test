from test_mocks.tests.import_a.import_b.m_b import func_b


def func_a(*args, **kwargs):

    return 1 + func_b(*args, **kwargs)

