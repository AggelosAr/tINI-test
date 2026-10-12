from test_about_shared.tests.test_imports_global_collisions.tests.import_a.import_b.m_b import (
    _why_func_b, func_b)
from tini_test import var


def func_a(*args, **kwargs):

    return 1 + func_b(*args, **kwargs)


def _why_func_a(*args, **kwargs):
    return 1 + var.A + _why_func_b(*args, **kwargs)