


def func_c(*args, **kwargs):

    return sum(args) + sum(kwargs.values())



def ___test_mocked_function(*args, **kwargs):
    return sum(args) + sum(kwargs.values())



#////////////////////////////////////
def ___test_mocking_in_outside_function(*args, **kwargs):
    from tini_test import Mock, must_equal, var
    with Mock.mocking(___test_mocked_function, args=(5, 5), kwargs={'k_val_1': 5}):
        result = ___test_mocked_function('?')
    must_equal(15, result)
    return result
#////////////////////////////////////





def C_open(*args, **kwargs):
    with open('?') as f:
        return f.read()


def C_open_MOCKING(*args, **kwargs):
    from tini_test import Mock, must_equal, var

    with open(var.root, 'r') as f:
        must_equal('inside C', f.read())

    with Mock.mocking(open, args=(var.root, 'r')) as f:
        with open('?') as f:
            res = f.read()

    with open(var.root, 'r') as f:
        must_equal('inside C', f.read())

    return res




#////////////////////////////////////


def _len(*args, **kwargs):
   #  print('GOT ', args, kwargs, ' ---- > ', len(args), ' --- ', len(kwargs))

    return len(args) + len(kwargs)



def xyz(args):
    return len(args)

def _xyz(*args, **kwargs):
    print('GOT ', args, kwargs, ' ---- > ', len(args), ' --- ', len(kwargs))
    return xyz(args) + xyz(kwargs)


#////////////////////////////////////
