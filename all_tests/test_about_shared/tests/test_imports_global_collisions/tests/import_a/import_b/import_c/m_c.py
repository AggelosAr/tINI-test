from tini_test import var


def func_c(*args, **kwargs):

    
    return sum(args) + sum(kwargs.values())



def _why_func_c(*args, **kwargs):

    
    return var.int + sum(args) + sum(kwargs.values())


def _why_func_c__C(*args, **kwargs):

    return 1 + var.C + sum(args) + sum(kwargs.values())