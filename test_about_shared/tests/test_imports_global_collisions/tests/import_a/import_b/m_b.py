from test_about_shared.tests.test_imports_global_collisions.tests.import_a.import_b.import_c.m_c import (
    _why_func_c, _why_func_c__C, func_c)
from tini_test import var


def func_b(*args, **kwargs):

    return 1 + func_c(*args, **kwargs)


def _why_func_b(*args, **kwargs):
    return 1 + var.B + _why_func_c__C(*args, **kwargs)